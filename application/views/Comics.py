from flask.views import MethodView


class SearchComic(MethodView):
    def get(self):
        return 'tests'

    def post(self):
        return 'test'


class AsignComic(MethodView):
    def post(self):
        return 'assigned'


class ViewAssignedComics(MethodView):
    def get(self):
        return 'comics'
