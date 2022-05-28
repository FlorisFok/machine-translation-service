FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

# Dowload lang detect model
RUN python -c "from ftlangdetect import detect;  detect('this is to dowload the model')"
RUN python -m textblob.download_corpora

ENV DEBUGMODE='off'
ENV PYENV='python'

CMD python app.py