from application.utils.marvelapi import MarvelAPI


class Characters():
    def __init__():
        return 'ok'

    def get_characters(params=''):
        response_characters = []

        response_api = MarvelAPI.make_request(
            endpoint='characters', params=params
        )

        response_json = response_api.json()

        for result in response_json['data']['results']:
            image = Characters.get_image(result['thumbnail'])

            response_characters.append({
                'id': result['id'],
                'name': result['name'],
                'image': image,
                'appearances': result['comics']['available']
            })
        return response_characters

    def get_image(result={}):
        path = result['path']
        extension = result['extension']
        return f'{path}.{extension}'
