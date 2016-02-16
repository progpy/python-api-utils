# coding: utf-8

import requests

VK_TIMEOUT = 60

url = 'https://api.vk.com/method/users.get'


def get_user_photo_id_or_none(user_id):
    try:
        response = requests.get(
            url,
            params={'user_id': user_id, 'count': 0,
                    'version': '3.0', 'fields': 'photo_50'},
            timeout=VK_TIMEOUT
        )
        response.raise_for_status()
        info = response.json()

        return info['response'][0]['photo_50']
    except Exception:
        return None
