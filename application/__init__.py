from flask import Flask
from application.routes import index, user


def create_app():
    app = Flask(__name__)

    app.add_url_rule("/", view_func=index.Index.as_view("index"))
    
    app.add_url_rule("/searchComics", view_func=index.Index.as_view("index"))

    app.add_url_rule("/users", view_func=index.Index.as_view("index"))

    app.add_url_rule("/addToLayaway", view_func=index.Index.as_view("index"))

    app.add_url_rule("/getLayawayList", view_func=index.Index.as_view("index"))

    return app
