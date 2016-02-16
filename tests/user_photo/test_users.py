# -*- coding: utf-8 -*-

import mock
import pytest
import requests

from user_photo.users import get_user_photo_id_or_none


@pytest.mark.parametrize('user_id, get_user_photo_id_or_none', [(53083705, 'http://cs5654.vk.me/u53083705/e_664a56e5.jpg'), (45269508, 'http://cs627828.vk.me/v627828508/c79b/bPMTCLUuKN0.jpg')])
def test_get_user_photo_id_or_none(user_id, url_in_response):
    """Тестируем логику user_photo_id"""
    json_return_value = {
        'response': [{'photo_50': url_in_response}]}
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.return_value = mock_of_response = mock.Mock()
        mock_of_response.json.return_value = json_return_value

        number_of_followers = get_user_photo_id_or_none(user_id=user_id)
        assert number_of_followers == url_in_response

        # Проверяем, что requests.get вызывается с нужным параметром
        __, kwargs = mock_of_requests_get.call_args_list[0]
        params_kwarg = kwargs['params']
        assert params_kwarg['user_id'] == user_id


def test_get_user_photo_id_or_none_with_error():
    """Тестируем get_user_photo_id_or_none при возникновении ошибки"""
    user_id = 1
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.side_effect = requests.exceptions.HTTPError()
        assert get_user_photo_id_or_none(user_id) is None

        # Проверяем, что requests.get вызывается с нужным параметром
        __, kwargs = mock_of_requests_get.call_args_list[0]
        params_kwarg = kwargs['params']
        assert params_kwarg['user_id'] == user_id
