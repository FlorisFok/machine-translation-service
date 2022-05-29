# Machine Translation Service
Translation flask API for the Helsinki NLP models available in the [Huggingface Transformers library](https://huggingface.co/Helsinki-NLP). 

## Start

With docker:

```
docker build -t machine-translation-service:<tag> .
docker run -p <port>:5000 -v /home/dtn/TranslationData:/app/data --gpus '"device=<gpu>"' -d --name translate machine-translation-service:<tag> 
```

## Use

APIs:
- get:/supported_languages -> returns list of supported languages
- get:/missing_languages -> returns list of languages it did not have but did detect
- post:/dowload_model -> {"source":"lang1", "target":"lang2"}, dowloads the model in the background.
- post:/detect -> {"text":"text"}, only detects the languages of the text
- post:/translate -> {"source":"lang1", "target":"lang2", "text":"text"}, translate text from, to given language. 
- post:/translate -> {"target":"lang2", "text":"text"}, translate text to given language from detected language. 

Call the service with curl:
```
curl --location --request POST 'http://localhost:5000/translate' \
--header 'Content-Type: application/json' \
-d '{
 "text":"hello",
 "source":"en",
 "target":"fr"
}'
```
## Test
Run simple test if all works, Check for "RUNNING ON: cuda" in logs to check if gpu is working.
```
docker exec machine-translation-service:<tag> python basic_test.py 
```
