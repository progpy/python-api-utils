#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rss.py
#  
#  Copyright 2016 don_vanchos <hozblok@gmail.com>
#  

import mock
import pytest
import requests

from ya_translate.translate import get_translate_or_none


@pytest.mark.parametrize('text, word_in_response', [("Яблоко", "Apple"), ("Привет", "Hi")])
def test_get_translate_or_none(text, word_in_response):
    """Тестируем логику get_number_of_followers_or_none"""
    json_return_value = {"code": 200, "lang": "ru-en", "text": [word_in_response]}
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.return_value = mock_of_response = mock.Mock()
        mock_of_response.json.return_value = json_return_value

        word_res = get_translate_or_none(text=text)
        assert word_res == word_in_response

        # Проверяем, что requests.get вызывается с нужным параметром
        __, kwargs = mock_of_requests_get.call_args_list[0]
        params_kwarg = kwargs['params']
        assert params_kwarg['text'] == text


def test_get_translate_or_none_with_error():
    """Тестируем get_number_of_followers_or_none при возникновении ошибки"""
    text = "Моль"
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.side_effect = requests.exceptions.HTTPError()
        assert get_translate_or_none(text) is None
        
        # Проверяем, что requests.get вызывается с нужным параметром
        __, kwargs = mock_of_requests_get.call_args_list[0]
        params_kwarg = kwargs['params']
        assert params_kwarg['text'] == text

