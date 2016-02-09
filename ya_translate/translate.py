#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rss.py
#  
#  Copyright 2016 don_vanchos <hozblok@gmail.com>
#  

import requests


TRANSLATE_TIMEOUT = 60

TRANSLATE_URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"

KEY_TRANSLATE = "trnsl.1.1.20160204T154320Z.58d11c2c1fa7d84b.e7fb2ff80125f5e2dd59c81bdfc1232620e5bc47"

def get_translate_or_none(text):
    direction='en'
    try:
        response = requests.get(
            TRANSLATE_URL,
            params={'key': KEY_TRANSLATE, 'text': text, 'lang': direction},
            timeout=TRANSLATE_TIMEOUT
        )
        response.raise_for_status()
        result_dict_text = response.json()
        return result_dict_text['text'][0]
    except Exception:
        return None
