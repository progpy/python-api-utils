# coding: utf-8

import requests
import requests.exceptions

VK_TIMEOUT = 60

GET_METHOD_URL_TEMPLATE = 'https://api.vk.com/method/{method_name}'


def get_number_of_followers_or_none(user_id):
    get_followers_url = GET_METHOD_URL_TEMPLATE.format(method_name='users.getFollowers')
    try:
        response = requests.get(
            get_followers_url,
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
            GET_METHOD_URL_TEMPLATE.format(method_name='users.get'),
            params={'user_id': user_id, 'version': '5.44'},
            timeout=VK_TIMEOUT
        )
        response.raise_for_status()
        user_name = response.json()['response'][0]
        return user_name['first_name'] + " " + user_name['last_name']
    except Exception:
        return None


def get_male_female_friends_count(user_id):
    get_friends_url = GET_METHOD_URL_TEMPLATE.format(method_name='friends.get')
    users_friends = requests.get(
        get_friends_url,
        params={'user_id': user_id, 'order': 'name', 'fields': 'sex'},
        timeout=VK_TIMEOUT
    )
    try:
        users_friends.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    users_friends_json = users_friends.json()
    all_friends = users_friends_json['response']
    male_female_friends_count = {'female': 0, 'male': 0}
    if all_friends:
        for friend in all_friends:
            if friend['sex'] == 1:
                male_female_friends_count['female'] += 1
            elif friend['sex'] == 2:
                male_female_friends_count['male'] += 1
    return male_female_friends_count
