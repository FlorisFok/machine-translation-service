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
- post:/v1/dowload_model -> {"source":"lang1", "target":"lang2"}, dowloads the model in the background.
- post:/v1/detect -> {"text":"text"}, only detects the languages of the text
- post:/v1/translate -> {"source":"lang1", "target":"lang2", "text":"text"}, translate text from, to given language. 
- post:/v1/translate -> {"target":"lang2", "text":"text"}, translate text to given language from detected language. 

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


# Benchmark

For each source (language) we calculated the BLEU score for translating 200 text pieces.
file source: 'https://dl.fbaipublicfiles.com/laser/WikiMatrix/v1/WikiMatrix.en-{source}.tsv.gz'
file format: source_{source}.text

Score: source_it.txt
Score Marian: 56.05 BLEU in 53 sec
Score Argos: 54.25 BLEU in 98 sec
Score deepl: 59.17 BLEU in 94.90 sec
Score: source_es.txt
Score Marian: 58.72 BLEU in 58.69 sec
Score Argos: 57.92 BLEU in 96.41 sec
Score deepl: 64.62 BLEU in 93.52 sec
Score: source_id.txt
Score Marian: 37.31 BLEU in 55.6 sec
Score Argos: 28.80 BLEU in 106.66 sec
Score deepl: 49.02 BLEU in 101.00 sec
Score: source_zh.txt
Score Marian: 27.31 BLEU in 50.307 sec
Score Argos: 16.95 BLEU in 106.56 sec
Score deepl: 38.58 BLEU in 89.64 sec
Score: source_fr.txt
Score Marian: 61.21 BLEU in 45.37 sec
Score Argos: 57.63 BLEU in 81.17 sec
Score deepl: 55.39 BLEU in 77.29 sec
Score: source_pt.txt
Score Marian: 0.64 BLEU in 7.36 sec
Score Argos: 60.87 BLEU in 100.88 sec
Score deepl: 63.86 BLEU in 104.20 sec
Score: source_ru.txt
Score Marian: 44.83 BLEU in 66.47 sec
Score Argos: 41.82 BLEU in 104.75 sec
Score deepl: 52.74 BLEU in 90.95 sec
Score: source_hi.txt
Score Marian: 21.88 BLEU in 59.13 sec
Score Argos: 34.22 BLEU in 110.79 sec
Score deepl: 0.52 BLEU in 185.95 sec
Score: source_tr.txt
Score Marian: 30.01 BLEU in 60.80 sec
Score Argos: 21.55 BLEU in 113.04 sec
Score deepl: 42.76 BLEU in 91.74 sec
Score: source_sv.txt
Score Marian: 53.14 % in 56.40 sec
Score Argos: 46.47 % in 188.30 sec
Score deepl: 56.39 % in 298.32 sec
Score: source_pl.txt
Score Marian: 45.54 % in 61.801 sec
Score Argos: 28.25 % in 102.30 sec
Score deepl: 52.14 % in 782.35 sec
Score: source_nl.txt
Score Marian: 52.94 % in 53.87 sec
Score Argos: 37.48 % in 100.60 sec
Score deepl: 55.95 % in 418.09 sec
