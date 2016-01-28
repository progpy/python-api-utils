# -*- coding: utf-8 -*-

import mock
import pytest
import requests

from vk.users import get_number_of_followers_or_none


@pytest.mark.parametrize('user_id, number_of_followers_in_response', [(1, 100500), (2, 0)])
def test_get_number_of_followers_or_none(user_id, number_of_followers_in_response):
    """Тестируем логику get_number_of_followers_or_none"""
    json_return_value = {'response': {'count': number_of_followers_in_response}}
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.return_value = mock_of_response = mock.Mock()
        mock_of_response.json.return_value = json_return_value

        number_of_followers = get_number_of_followers_or_none(user_id=user_id)
        assert number_of_followers == number_of_followers_in_response

        # Проверяем, что requests.get вызывается с нужным параметром
        __, kwargs = mock_of_requests_get.call_args_list[0]
        params_kwarg = kwargs['params']
        assert params_kwarg['user_id'] == user_id


def test_get_number_of_followers_or_none_with_error():
    """Тестируем get_number_of_followers_or_none при возникновении ошибки"""
    user_id = 42
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.side_effect = requests.exceptions.HTTPError()
        assert get_number_of_followers_or_none(user_id) is None

        # Проверяем, что requests.get вызывается с нужным параметром
        __, kwargs = mock_of_requests_get.call_args_list[0]
        params_kwarg = kwargs['params']
        assert params_kwarg['user_id'] == user_id
