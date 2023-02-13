import os
import hashlib


class MarvelAPI():

    def __init__():
        return 'ok'

    def get_hash(timestamp=None):
        from application import app
        try:
            public_key = os.getenv('MARVEL_PUBLICKEY').encode()
            private_key = os.getenv('MARVEL_PRIVATEKEY').encode()

            hash_md5 = hashlib.md5()
            hash_md5.update(timestamp)
            hash_md5.update(private_key)
            hash_md5.update(public_key)

            return hash_md5.hexdigest()
        except Exception as e:
            app.logger.error(f'MarvelAPI.get_hash {e}')
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
        from application import app
        url = MarvelAPI.get_url(
            endpoint=endpoint,
            params=params,
            order_by=order_by)

        app.logger.debug(f'MarvelAPI.make_request {url}')
        payload = {}
        headers = {}
        try:
            response = requests.request(
                method='GET',
                url=url,
                headers=headers,
                data=payload,
                timeout=10
            )
        except Exception as error:
            app.logger.error('MarvelAPI.make_request', error)
            raise Exception('Request error')

        if 400 <= response.status_code < 500:
            app.logger.warning('MarvelAPI.make_request', response.status_code)
            raise Exception('Marvel data not found')

        elif 500 <= response.status_code < 600:
            app.logger.warning('MarvelAPI.make_request', response.status_code)
            raise Exception('Marvel API not working')

        app.logger.debug('MarvelAPI.make_request', response.status_code)    
        return response
