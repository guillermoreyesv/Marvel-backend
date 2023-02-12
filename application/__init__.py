from flask import Flask
from application.views import Index, User, Comics
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
import logging


app = Flask(__name__)
load_dotenv()

app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

if os.getenv('RECORD_LOG'):
    level_debug = logging.WARNING
    if os.getenv('APP_MODE') == 'debug':
        level_debug = logging.DEBUG
    logging.basicConfig(level=level_debug,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        filename='example.log',
                        filemode='w')


# INDEX
app.add_url_rule(
    rule='/',
    methods=['GET'],
    view_func=Index.Index.as_view('index')
)

# Search Marvel Comics
app.add_url_rule(
    rule='/searchComics',
    methods=['GET'],
    view_func=Comics.SearchComic.as_view('searchComics')
)

# Register and check profile user
app.add_url_rule(
    rule='/users',
    methods=['GET', 'POST'],
    view_func=User.ManageUser.as_view('users')
)

# Login
app.add_url_rule(
    rule='/users/login',
    methods=['POST'],
    view_func=User.Login.as_view('usersLogin')
)

# Assign comics to an user
app.add_url_rule(
    rule='/addToLayaway',
    methods=['POST'],
    view_func=User.AsignComic.as_view('addToLayaway')
)

# View assigned comics
app.add_url_rule(
    rule='/getLayawayList',
    methods=['GET'],
    view_func=User.ViewAssignedComics.as_view('getLayawayList')
)
