import json
import os

import requests

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if GOOGLE_API_KEY is None:
    raise ValueError('GOOGLE_API_KEY should not be None')

response = requests.post(
    url='https://translation.googleapis.com/language/translate/v2',
    params={
        'q': "Bonjour à vous!",
        'source': 'fr',
        'target': 'en',
        'format': 'text',
        'key': GOOGLE_API_KEY,
    }
)
print(response.json())
# {'data': {'translations': [{'translatedText': 'Hello to you!'}]}}

response = requests.post(
    url='https://translation.googleapis.com/language/translate/v2',
    params={
        'q': json.dumps([
            "Bonjour à vous!",
            "Comment allez-vous?",
            "Les API REST, c'est cool!"
        ]),
        'source': 'fr',
        'target': 'en',
        'format': 'text',
        'key': GOOGLE_API_KEY,
    }
)
print(response.json())
# {'data': {'translations': [{'translatedText': '["Hello there!", "How are you?", "REST APIs are cool!"]'}]}}
