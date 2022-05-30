import os
from flask import Flask, request, jsonify
from translate import Translator, QUEUE
from config import *
from ftlangdetect import detect
from flask_pydantic import validate # To be implemented
from torch.cuda import is_available
from apscheduler.schedulers.background import BackgroundScheduler
from storage import ElasticStorage, send_

def save_queue():
    """Clear queue, push to web_metrics"""
    global QUEUE

    if len(QUEUE) > 0:
        opensearch.bulk_store(opensearch.database, payload=QUEUE, method='add')
        QUEUE = []

# CUDA CHECK
device = "cuda" if is_available() else 'cpu'
print('RUNNING ON:', device)

# Classes
app = Flask(__name__)
translator = Translator(MODEL_PATH, device)
opensearch = ElasticStorage()
scheduler = BackgroundScheduler()

# Settings
app.config["DEBUG"] = True if os.getenv('DEBUGMODE', 'on') == 'on' else False
python_env = os.getenv("PYENV", 'python3')
interval_min = int(os.getenv("DB_INTER_MIN", '60'))

# Tracking of langs
MISSED = set()
HAVE = set([i[0] for i in translator.get_supported_langs()])

@app.route('/healthcheck', methods=["GET"])
def health_check():
    """Confirms service is running"""
    return "ok"

@app.get("/scheduler_update")
def scheduler_update():
    """Get update now!"""
    save_queue()
    return 'ok'

@app.get("/toggletimer")
def timertoggle():
    """"""
    global translator, JOB, scheduler
    
    if translator.timer:
        save_queue()
        JOB.remove()
        scheduler.stop()
    else:
        JOB = scheduler.add_job(save_queue, 'interval', minutes=interval_min)
        scheduler.start()

    translator.timer = False if translator.timer else True
    return "Timer is " + ('on' if translator.timer else 'off')

@app.route('/supported_languages', methods=["GET"])
def get_supported_languages():
    """Returns list of supported languages"""
    langs = translator.get_supported_langs()
    return jsonify({"output":langs})

@app.route('/missing_languages', methods=["GET"])
def get_missing_languages():
    """Returns list of missing languages"""
    return jsonify({"output":list(MISSED)})

@app.route('/v1/dowload_model', methods=["POST"])
def dowload_model():
    """Dowload model, check after download if succesful"""
    source = request.json['source']
    target = request.json['target']

    if source in MISSED:
        MISSED.remove(source)

    HAVE.add(source)
    os.popen(f"{python_env} download_models.py --source {source} --target {target}")

    return jsonify({"output":'Trying to download it'}) 

@app.route('/v1/detect', methods=["POST"])
def detect_language():
    """Use detection standalone"""
    return jsonify(detect(request.json['text'].replace('\n', ' ')))

@app.route('/v1/translate', methods=["POST"])
def get_prediction():
    """Translate incoming strings: if it was a success the results will start with "success..."""
    global MISSED

    # Always here
    target = request.json['target']
    text = request.json['text']

    # Guess or Force
    if 'source' in request.json:
        source = request.json['source']
    else:
        detdict = detect(text.replace('\n', ' '))
        source = detdict['lang']
    
    # Custom batchsize for testing
    if 'batch_size' in request.json:
        batch_size = int(request.json['batch_size'])
    else:
        batch_size = NORMAL_BATCH_SIZE

    # Save have nots
    if source not in HAVE:
        MISSED.add(source)

    # Skip same langauges
    if source == target:
        return jsonify({"results":'Source is equal to target', "output":text, 'source':target})
    
    # Translate
    translation, message = translator.translate(source, target, text, batch_size)
    return jsonify({"results":message, "output":translation, 'source':source})


@app.errorhandler(500)
def internal_error(error):
    send_("TRANSLATION 500 ERROR: " + str(error))
    return jsonify({"results":'OOPS', 'status_code':500})


if __name__ == '__main__':
    # Add https support
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))