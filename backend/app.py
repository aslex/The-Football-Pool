from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import json
from functools import wraps
from jose import jwt
from werkzeug import exceptions
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from .auth.auth import requires_auth_permission
from .database.models import setup_db, drop_and_create_all, User, Game, Week
import requests
from datetime import date
import xmltodict
import json
from urllib.request import urlopen

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "localhost:3000"}})

setup_db(app)
# CORS(app)
drop_and_create_all()

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


@app.route('/', methods=['GET'])
def get_current_scores():
    # DEPRECATED !  DO NOT USE
    # res = requests.get('http://www.nfl.com/ajax/scorestrip?season=2019&seasonType=REG&week=2', headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"})

    res = requests.get('https://feeds.nfl.com/feeds-rs/scores.json')
    return res.json()

    print('raw res:', res.text)
    res_parse = xmltodict.parse(res.text)
    res_json = json.dumps(res_parse)
    return res_json
    # if res.status_code != 200:
    #     return f'error: {res.status_code}'
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    return f'year, month'

@app.route('/users/<id>', methods=['PATCH'])
@requires_auth_permission(permission='post:pics')
def update_nickname(payload, id, permission='post:pics'):
    print(f'id ? {id}')
    print(f'permissions ?', {permission})
    print(f'payload ? {payload}')

    user = User.query.filter_by(id = payload.sub.id)
    if not user:
        abort(404)
    else:
        try:
            user.update()

        except:

    return json.dumps({'message':'nickname has been updated' })

@app.route('/picks', methods=['GET', 'POST', 'PATCH'])
@requires_auth_permission('post:pics')
def submit_picks(permission):
    # unpack request header
    # token = get_token_auth_header()
    # payload = verify_decode_jwt(token)

    print('user : ', payload["sub"])
    if request.method == 'POST':
        print('save picks to db')
    elif request.method == 'GET':
        print('show submitted picks')
    return 'submit your picks'

