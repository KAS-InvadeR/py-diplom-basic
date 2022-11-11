import requests


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_foto(self, id_user_photo, album_id, count=15):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': id_user_photo, 'album_id': album_id, 'extended': '1', 'photo_sizes': '1', 'count': count}
        response = requests.get(url, params={**self.params, **params})
        return response.json()
