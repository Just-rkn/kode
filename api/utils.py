import requests

from kode.settings import SPELLER_URL


def check_spelling(text: str) -> list[dict]:
    params = {
        'text': text,
        'lang': 'ru'
    }
    response = requests.get(url=SPELLER_URL, params=params)
    response.raise_for_status()
    return response.json()
