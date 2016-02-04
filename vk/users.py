# coding: utf-8

import requests

VK_TIMEOUT = 60

GET_FOLLOWERS_URL = 'https://api.vk.com/method/users.getFollowers'
GET_USERNAME_URL = 'https://api.vk.com/method/users.get'


def get_number_of_followers_or_none(user_id):
    try:
        response = requests.get(
            GET_FOLLOWERS_URL,
            params={'user_id': user_id, 'count': 0, 'version': '3.0'},
            timeout=VK_TIMEOUT
        )
        response.raise_for_status()
        followers_info = response.json()
        return followers_info['response']['count']
    except Exception:
        return None


def get_username_by_id_or_none(user_id):
    try:
        response = requests.get(
            GET_USERNAME_URL,
            params={'user_id': user_id, 'version': '5.44'},
            timeout=VK_TIMEOUT
        )
        response.raise_for_status()
        user_name = response.json()['response'][0]
        return user_name['first_name'] + " " + user_name['last_name']
    except Exception:
        return None
