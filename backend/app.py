from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import json
from functools import wraps
from jose import jwt
from werkzeug import exceptions
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from .auth.auth import requires_auth_permission
from .database.models import setup_db, create_all, User

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

setup_db(app)
# CORS(app)
create_all()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


# @app.route('/', methods=['GET'])
# def home_page():
#     return 'welcome !'


@app.route('/picks', methods=['GET', 'POST', 'PATCH'])
@requires_auth_permission('post:pics')
def submit_picks(permission):
    # unpack request header
    token = get_token_auth_header()
    payload = verify_decode_jwt(token)

    print('user : ', payload["sub"])
    if request.method == 'POST':
        print('save picks to db')
    elif request.method == 'GET':
        print('show submitted picks')
    return 'submit your picks'
