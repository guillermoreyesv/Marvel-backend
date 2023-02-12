from flask import Flask
from application.views import Index, User, Comics
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


# INDEX
app.add_url_rule(
    rule="/",
    methods=['GET'],
    view_func=Index.Index.as_view("index")
)

# Search Marvel Comics
app.add_url_rule(
    rule="/searchComics",
    methods=['GET'],
    view_func=Comics.SearchComic.as_view("searchComics")
)

# Register and check profile user
app.add_url_rule(
    rule="/users",
    methods=['GET', 'POST'],
    view_func=User.ManageUser.as_view("users")
)

# Login
app.add_url_rule(
    rule="/users/login",
    methods=['POST'],
    view_func=User.Login.as_view("usersLogin")
)

# Assign comics to an user
app.add_url_rule(
    rule="/addToLayaway",
    methods=['POST'],
    view_func=Comics.AsignComic.as_view("addToLayaway")
)

# View assigned comics
app.add_url_rule(
    rule="/getLayawayList",
    methods=['GET'],
    view_func=Comics.ViewAssignedComics.as_view("getLayawayList")
)
