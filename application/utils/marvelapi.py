import os
import hashlib


class MarvelAPI():

    def __init__():
        return 'ok'

    def get_hash(timestamp=None):
        try:
            public_key = os.getenv('MARVEL_PUBLICKEY').encode()
            private_key = os.getenv('MARVEL_PRIVATEKEY').encode()

            hash_md5 = hashlib.md5()
            hash_md5.update(timestamp)
            hash_md5.update(private_key)
            hash_md5.update(public_key)

            return hash_md5.hexdigest()
        except Exception as e:
            print('Failed to generate marvel hash', e)
            exit()

    def get_url(endpoint='', params='', order_by=''):
        import time
        marvel_url = os.getenv('MARVEL_URL')
        apikey = os.getenv('MARVEL_PUBLICKEY')

        timestamp = str(time.time())
        timestamp_byte = bytes(timestamp, 'utf-8')

        hash = MarvelAPI.get_hash(timestamp=timestamp_byte)

        url = f'{marvel_url}{endpoint}?'
        url += f'&ts={timestamp}'
        url += f'&apikey={apikey}'
        url += f'&hash={hash}'
        url += f'&{params}' if params else ''
        url += f'&{order_by}' if order_by else ''

        return url

    def make_request(endpoint='', params='', order_by=''):
        import requests
        url = MarvelAPI.get_url(
            endpoint=endpoint,
            params=params,
            order_by=order_by)

        print(url)
        payload = {}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)
