from app import app, MODEL_PATH, translator, detect
import time
import subprocess as sp
import requests


def get_gpu_memory():
    command = "nvidia-smi --query-gpu=memory.free --format=csv"
    memory_free_info = sp.check_output(command.split()).decode('ascii').split('\n')[:-1][1:]
    memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
    return memory_free_values

free = get_gpu_memory()
client = app.test_client()

class TestTranslationAPI():
      # Test text
      basic_text  = 'Op 15 december 2021 werd het coalitieakkoord gepresenteerd. Het bevat onder meer afspraken over een versnelling van de Nederlandse klimaatambities (55% CO2-reductie in 2030), aanpassing van kinderopvangbekostiging, voorbereidingen voor nieuwe kerncentrales en invoering van het rekeningrijden vanaf 2030, versnelde stikstofreductie (-50% in 2030), afschaffen van de verhuurderheffing, verdere regulering van de vrije huursector, versterking van de sociale advocatuur, gelijktrekken van de lerarensalarissen in het basisonderwijs met die van het middelbaar onderwijs, een terugkeer van de basisbeurs, verhoging in termijnen wettelijk minimumloon met 7,5% en meer geld voor defensie.'

      def test_gets(self):
            out = client.get(f'/healthcheck')
            assert out.status_code == 200, 'Service is not running'

            out = client.get(f'/supported_languages').json
            assert 'nl' in [i[0] for i in out['output']], "NL not downloaded"

            out = client.get(f'/missing_languages').json
            assert out['output'] == [], "Test not done on new instance"

      def test_download_model(self):
            # Two models we need for the test
            res = client.post(f'/v1/dowload_model', json={'source':'fr', 'target':'en'})
            assert res.json['output'] == 'Trying to download it', "Could not trigger dowload"

            res = client.post(f'/v1/dowload_model', json={'source':'nl', 'target':'en'})
            assert res.json['output'] == 'Trying to download it', "Could not trigger dowload"
            
            have = ['']
            start_time = time.time()

            # Only continue if all are here
            while 'nl' not in have or 'fr' not in have:

                  # Check new languages
                  out = client.get(f'/supported_languages').json
                  have = [i[0] for i in out['output']]
                  
                  # Max wait time: 10min
                  if (time.time() - start_time) > 600:
                        raise Exception('Did not dowload')
                  
                  # Don't spam
                  time.sleep(1)


      def test_model_load(self):
            r = client.post(f'/v1/translate', 
                              json={'text':self.basic_text,
                                    'source':'fr', 'target':'en'})

            assert r.json['results'] == 'successfully loaded model for fr-en transation', "Loading from path failed"


      def test_model_swap(self):
            r = client.post(f'/v1/translate', 
                              json={'text':self.basic_text,
                                    'source':'nl', 'target':'en'})

            assert r.json['results'] == 'successfully loaded model for nl-en transation', 'CUDA swap was not succesful'

      def test_auto_detect(self):
            r = client.post('/v1/translate', 
                              json={'text':self.basic_text,
                                    'target':'en'})

            assert r.json['results'] == 'success', 'Two same samples didnt worked without trouble'
            assert r.json['source'] == 'nl', 'Not able to detect correct languages'


class TestTranslationClass():

      html = requests.get('https://projects.haykranen.nl/dummytekst/').text
      i = html.find('<textarea')
      websitetext = html[i + html[i:].find('>'): html.find('</textarea')]

      basic_text = 'Op 15 december 2021 werd het coalitieakkoord gepresenteerd.'
      basic_response = 'On 15 December 2021, the coalition agreement was presented.'

      def test_load(self):
            pass

      def test_translate(self):
            response = translator.translate('nl', 'en', self.basic_text)
            assert response[0] == self.basic_response, "Translation was not succesful"

      def test_traslate_large(self):
            response = translator.translate('nl', 'en', self.websitetext * 4, 10)
            assert len(response[0]) > len(self.websitetext * 4) * 0.75, "Translation was not completely processed"

      def test_swap(self):
            _ = translator.translate('fr', 'en', self.basic_text)
            assert 'fr-en' in translator.models, "Model not loaded"

      def test_gpu_monitor(self):
            free2 = get_gpu_memory()
            assert free2[0] < free[0], 'No gpu is used'


class TestLangDetect():

      basic_text = basic_text  = 'Op 15 december 2021 werd het coalitieakkoord gepresenteerd. Het bevat onder meer afspraken over een versnelling van de Nederlandse klimaatambities (55% CO2-reductie in 2030), aanpassing van kinderopvangbekostiging, voorbereidingen voor nieuwe kerncentrales en invoering van het rekeningrijden vanaf 2030, versnelde stikstofreductie (-50% in 2030), afschaffen van de verhuurderheffing, verdere regulering van de vrije huursector, versterking van de sociale advocatuur, gelijktrekken van de lerarensalarissen in het basisonderwijs met die van het middelbaar onderwijs, een terugkeer van de basisbeurs, verhoging in termijnen wettelijk minimumloon met 7,5% en meer geld voor defensie.'

      def test_lang_detet(self):
            out = detect(self.basic_text)
            assert out['lang'] == 'nl', "Not able to detect proper langauges" 