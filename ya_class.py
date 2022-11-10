import requests
from pprint import pprint


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload_path(self, new_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        parametrs = {'path': new_path}
        headers = {'Authorization': f'OAuth {self.token}'}
        request_url = requests.put(url, params=parametrs, headers=headers)
        if request_url.status_code == 201:
            print('Папка создана!')

    def upload_foto(self, url_i, new_path_name):
        url_u = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        parametrs_u = {'url': url_i, 'path': new_path_name}
        headers_u = {'Authorization': f'OAuth {self.token}'}
        upload_foto = requests.post(url_u, params=parametrs_u, headers=headers_u)
        # pprint(upload_foto)

        # response = requests.put(request_url['href'], data=open(file_name, 'rb'))
        # if response.status_code == 201:
        #     print('Success')
        # else:
        #     print('Error')
