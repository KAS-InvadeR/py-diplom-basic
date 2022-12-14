import datetime
import time
from pprint import pprint

from tqdm import tqdm
from collections import OrderedDict

from vk_class import VK
from ya_class import YaUploader


def fhoto_vk():
    user_id = '4932860'
    with open('vk_token.txt', 'r') as file_object_vk:
        token_vk = file_object_vk.read().strip()

    # id_user_photo = '730286'
    # album_id = 'profile'
    # new_path = 'new'
    id_user_photo = input('Введите ID пользователя: ')
    album_id = input('Введите ID альбома с фотографиями или команду\n'
                     '"wall" — фотографии со стены\n"profile" — фотографии профиля\n')
    new_path = input('Введите название папки для копирование фото на ваш яндекс.диск:')
    vk = VK(token_vk, user_id)
    fotos_profile = vk.users_foto(id_user_photo, album_id)
    return fotos_profile, new_path


def sort_foto(fotos_profile):
    all_fhotos_z = {}
    for foto_profile in tqdm(fotos_profile['response']['items'], ncols=100, desc='Получение фотографий профиля'):
        for foto_size in foto_profile['sizes']:
            if foto_size['type'] == 'z':
                if foto_profile['likes']['count'] in list(all_fhotos_z.keys()):
                    data = (datetime.datetime.fromtimestamp(foto_profile['date'])).strftime('%Y-%m-%d')
                    temp = str(foto_profile['likes']['count']) + '_' + str(data)
                    size = (foto_size['height'] + foto_size['width'])
                    all_fhotos_z[temp] = {'size': size, 'url': foto_size['url'],
                                          'data': data, 'type': foto_size['type']}
                else:
                    data = (datetime.datetime.fromtimestamp(foto_profile['date'])).strftime('%Y-%m-%d')
                    size = (foto_size['height'] + foto_size['width'])
                    all_fhotos_z[foto_profile['likes']['count']] = {'size': size,
                                                                    'url': foto_size['url'],
                                                                    'data': data,
                                                                    'type': foto_size['type']}
    return all_fhotos_z


def big_fotos(all_fhotos_z):
    all_fhotos_json = []
    top_fotos = OrderedDict(sorted(all_fhotos_z.items(), key=lambda t: t[1]['size'], reverse=True)[:5])
    finish_fotos = {}
    for key_ in top_fotos:
        finish_fotos[key_] = all_fhotos_z[key_]['url']
        dict_list = dict(
            [('file name', str(key_) + '.jpg'), ('size', all_fhotos_z[key_]['type'])])
        all_fhotos_json.append(dict_list)
    return finish_fotos, all_fhotos_json


def upload_ya(new_path, finish_fotos):
    with open('ya_token.txt', 'r') as file_object_ya:
        token_ya = file_object_ya.read().strip()

    yaupload = YaUploader(token_ya)
    yaupload.upload_path(new_path)
    for name, url in tqdm(finish_fotos.items(), ncols=100, desc='Загрузка фотографий на Яндекс.диск'):
        time.sleep(1)
        new_path_name = new_path + '/' + str(name) + '.jpg'
        yaupload = YaUploader(token_ya)
        yaupload.upload_foto(url, new_path_name)


if __name__ == '__main__':
    fotos_profile, new_path = fhoto_vk()

    all_fhotos_z = sort_foto(fotos_profile)
    finish_fotos, all_fhotos_json = big_fotos(all_fhotos_z)
    upload_ya(new_path, finish_fotos)
    print('Фото загружены, информация о фото ниже:')
    pprint(all_fhotos_json)