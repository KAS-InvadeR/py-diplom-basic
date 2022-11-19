import sys

import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload_path(self, new_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        parametrs = {'path': new_path}
        headers = {'Authorization': f'OAuth {self.token}'}
        response = requests.put(url, params=parametrs, headers=headers)
        if response.status_code == 201:
            print('Папка создана')
        else:
            print('Ошибка, папка не создана, проверти имя папки')
            sys.exit()

    def upload_foto(self, url_i, new_path_name):
        url_u = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        parametrs_u = {'url': url_i, 'path': new_path_name}
        headers_u = {'Authorization': f'OAuth {self.token}'}
        response = requests.post(url_u, params=parametrs_u, headers=headers_u)
        if response.status_code != 202:
            print('Ошибка загрузки')
