# coding: utf-8

import requests


VK_TIMEOUT = 60

GET_FOLLOWERS_URL = 'https://api.vk.com/method/users.getFollowers'


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
