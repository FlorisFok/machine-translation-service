import requests

# Test text
oefen = 'Op 15 december 2021 werd het coalitieakkoord gepresenteerd. Het bevat onder meer afspraken over een versnelling van de Nederlandse klimaatambities (55% CO2-reductie in 2030), aanpassing van kinderopvangbekostiging, voorbereidingen voor nieuwe kerncentrales en invoering van het rekeningrijden vanaf 2030, versnelde stikstofreductie (-50% in 2030), afschaffen van de verhuurderheffing, verdere regulering van de vrije huursector, versterking van de sociale advocatuur, gelijktrekken van de lerarensalarissen in het basisonderwijs met die van het middelbaar onderwijs, een terugkeer van de basisbeurs, verhoging in termijnen wettelijk minimumloon met 7,5% en meer geld voor defensie.'


out = requests.get(f'http://localhost:5000/supported_languages').json()
assert 'nl' in [i[0] for i in out['output']], "NL not downloaded"

out = requests.get(f'http://localhost:5000/missing_languages').json()
assert out['output'] == [], "Test not done on new instance"

r = requests.post(f'http://localhost:5000/translate', 
                  json={'text':oefen,
                        'source':'fr', 'target':'en'})

assert r.json()['results'] == 'successfully loaded model for fr-en transation', "Loading from path failed"


r = requests.post(f'http://localhost:5000/translate', 
                  json={'text':oefen,
                        'source':'nl', 'target':'en'})

assert r.json()['results'] == 'successfully loaded model for nl-en transation', 'CUDA swap was not succesful'

r = requests.post(f'http://localhost:5000/translate', 
                  json={'text':oefen,
                        'target':'en'})
out = r.json()
assert out['results'] == 'success', 'Two same samples didnt worked without trouble'
assert out['source'] == 'nl', 'Not able to detect correct languages'
