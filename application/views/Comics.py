from flask.views import MethodView
from flask import request


class SearchComic(MethodView):
    def get(self):
        # Library import
        from application.utils.comics import Comics
        from application.utils.characters import Characters

        # Default Values
        response_dict = {
            'characters': [],
            'comics': []
        }

        list_characters = ['character', 'characters']
        list_comics = ['comic', 'comics']

        # Get params
        keyword_param = request.args.get(key='keyword', default='')
        type_param = request.args.get(key='type', default='')

        # Get Characters
        if type_param in list_characters or not type_param:
            params = ''
            if keyword_param:
                params = f'nameStartsWith={keyword_param}'
            response_dict['characters'] = Characters.get_characters(
                params=params
            )

        # Get Comics
        if type_param in list_comics or not type_param:
            params = ''
            if keyword_param:
                params = f'titleStartsWith={keyword_param}'
            response_dict['comics'] = Comics.get_comics(
                params=params
            )

        return response_dict


class AsignComic(MethodView):
    def post(self):
        return 'assigned'


class ViewAssignedComics(MethodView):
    def get(self):
        return 'comics'
