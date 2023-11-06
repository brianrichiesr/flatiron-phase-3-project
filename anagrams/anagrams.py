#!/usr/bin/env python
import requests

def check_word(word):
    result = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    return result

is_word = check_word("back")
print(is_word.status_code)
