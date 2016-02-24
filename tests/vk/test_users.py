# -*- coding: utf-8 -*-

import mock
import pytest
import requests

from vk.users import get_number_of_followers_or_none, get_username_by_id_or_none, get_male_female_friends_count


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


@pytest.mark.parametrize('user_id, response_username', [(1, "Foo Bar"), (100, "Dead Beef")])
def test_get_username_by_id_or_none(user_id, response_username):
    """Тестируем логику get_username_by_id_or_none
    :param user_id: int request
    :param response_username: str response
    """
    name = response_username.split()
    json_return_value = {'response': [{"id": user_id, 'first_name': name[0], 'last_name': name[1]}]}
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.return_value = mock_of_response = mock.Mock()
        mock_of_response.json.return_value = json_return_value
        username = get_username_by_id_or_none(user_id=user_id)
        assert username == response_username


def test_get_username_by_id_or_none_with_error():
    """Тестируем get_username_by_id_or_none при возникновении ошибки"""
    user_id = 42
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.side_effect = requests.exceptions.HTTPError()
        assert get_username_by_id_or_none(user_id) is None


@pytest.mark.parametrize('user_id, female_count, male_count', [(5009988, 100, 200), (5009988, 0, 0)])
def test_get_male_female_friends_count(user_id, female_count, male_count):
    """Тестируем логику get_male_female_friends_count"""
    json_return_value = {"response": ([{'sex': 1}] * female_count) + ([{'sex': 2}] * male_count)}
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.return_value = mock_of_response = mock.Mock()
        mock_of_response.json.return_value = json_return_value

        male_female_friends_count = get_male_female_friends_count(user_id=user_id)
        assert (male_female_friends_count['female'] == female_count and male_female_friends_count['male'] == male_count)


def test_get_male_female_friends_count_with_error():
    """Тестируем get_male_female_friends_count при возникновении ошибки"""
    user_id = 42
    with mock.patch('requests.get') as mock_of_requests_get:
        mock_of_requests_get.side_effect = requests.exceptions.HTTPError()
        assert get_number_of_followers_or_none(user_id) is None
