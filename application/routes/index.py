from flask.views import MethodView


class Index(MethodView):
    def get(self):
        return 'test'

    def post(self):
        return 'test'
