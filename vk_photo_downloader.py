# -*- coding: utf-8 -*-
"""
Скрипт для скачивания музыки с сайта vkontakte.ru (vk.com)
Запуск:
python vkcom_audio_download.py
Принцип работы:
Скрипт проверяет сохраненный access_token. Если его нет или срок истек,
то открывается страница в браузере с запросом на доступ к аккаунту.
После подтверждения идет редирект на https://oauth.vk.com/blank.htm#... .
Нужно скопировать весь url, на который вас редиректнуло и вставить его
в консоль скрипта.
Далее будут скачиваться все ваши аудиозаписи. Если аудиозапись уже есть на
диске - то скачивания не происходит.
Будут запрошены ваши данные приложением с app_id = 3358129
Можно создать свое Standalone-приложение с доступом к аудио здесь:
http://vk.com/editapp?act=create
И заменить APP_ID на ваше.
"""
import pickle
import urllib
import webbrowser

import os
import re
import requests
from datetime import (datetime, timedelta)


# id of vk.com application, that has access to audio
from furl import furl
APP_ID = '6323170'
# if None, then save mp3 in current folder
MUSIC_FOLDER = 'music'
# file, where auth data is saved
AUTH_FILE = '.auth_data'
# chars to exclude from filename
FORBIDDEN_CHARS = '/\\\?%*:|"<>!'


def get_saved_auth_params():
    access_token = None
    user_id = None
    try:
        with open(AUTH_FILE, 'rb') as pkl_file:
            token = pickle.load(pkl_file)
            expires = pickle.load(pkl_file)
            uid = pickle.load(pkl_file)
        if datetime.now() < expires:
            access_token = token
            user_id = uid
    except IOError:
        pass
    return access_token, user_id


def save_auth_params(access_token, expires_in, user_id):
    print(access_token, expires_in, user_id)
    expires = datetime.now() + timedelta(seconds=int(expires_in))
    with open(AUTH_FILE, 'wb') as output:
        pickle.dump(access_token, output)
        pickle.dump(expires, output)
        pickle.dump(user_id, output)


def get_auth_params():
    auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                "&scope=audio&redirect_uri=http://oauth.vk.com/blank.html"
                "&display=page&response_type=token".format(app_id=APP_ID))
    print('Произошел переход по урлу:')
    print(auth_url)
    webbrowser.open_new_tab(auth_url)
    redirected_url = input("Вставьте урл после редиректа в вк:\n")

    f = furl(redirected_url)
    arguments = f.fragment.args
    save_auth_params(arguments['access_token'], arguments['expires_in'],
                     arguments['user_id'])
    return arguments['access_token'], arguments['user_id']

#
# def get_tracks_metadata(access_token, user_id):
#     # url = ("https://api.vkontakte.ru/method/audio.get.json?"
#     url = ("https://api.vk.com/method/audio.get.json?"
#            "uid={uid}&access_token={atoken}".format(
#                uid=user_id, atoken=access_token)
#            )
#     # audio_get_page = urllib2.urlopen(url).read()
#     response = requests.get(url)
#     return response.json()['response']
    # return json.loads(audio_get_page)['response']
def get_tracks_metadata(access_token, user_id):
    # url = ("https://api.vkontakte.ru/method/audio.get.json?"
    url = ("https://api.vk.com/method/album.get.json?"
           "uid={uid}&access_token={atoken}".format(
               uid=user_id, atoken=access_token)
           )
    # audio_get_page = urllib2.urlopen(url).read()
    response = requests.get(url)
    return response.json()['response']
    # return json.loads(audio_get_page)['response']


def get_track_full_name(t_data):
    import HTMLParser

    html_parser = HTMLParser.HTMLParser()
    full_name = u"{0}_{1}".format(
        html_parser.unescape(t_data['artist'][:100]).strip(),
        html_parser.unescape(t_data['title'][:100]).strip(),
    )
    full_name = re.sub('[' + FORBIDDEN_CHARS + ']', "", full_name)
    full_name = re.sub(' +', ' ', full_name)
    return full_name + ".mp3"


def download_track(t_url, t_name):
    t_path = os.path.join(MUSIC_FOLDER or "", t_name)
    if not os.path.exists(t_path):
        print("Downloading {0}".format(t_name.encode('ascii', 'replace')))
        urllib.urlretrieve(t_url, t_path)


def main():
    access_token, user_id = get_saved_auth_params()
    if not access_token or not user_id:
        access_token, user_id = get_auth_params()
    # tracks = get_tracks_metadata(access_token, user_id)


    if MUSIC_FOLDER and not os.path.exists(MUSIC_FOLDER):
        os.makedirs(MUSIC_FOLDER)
    for t in tracks:
        t_name = get_track_full_name(t)
        download_track(t['url'], t_name)
    print("All music is up to date")


if __name__ == '__main__':
    main()
