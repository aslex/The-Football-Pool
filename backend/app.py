from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import json
from functools import wraps
from jose import jwt
from werkzeug import exceptions
from werkzeug.exceptions import HTTPException
from urllib.request import urlopen
from flask_cors import CORS

from .database.models import setup_db, create_all, User

app = Flask(__name__)

setup_db(app)
CORS(app)
create_all()


# auth
AUTH0_DOMAIN = 'the-football-pool.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fbpool'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


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


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        return exceptions.Unauthorized()
        # raise AuthError({
        #     'code': 'authorization_header_missing',
        #     'description': 'Authorization header is expected.'
        # }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    print('urlopen working')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 400)
    if permission not in payload['permissions']:
        abort(403)
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found'
        }, 403)
    return True


def requires_auth_permission(permission=''):
    def requires_auth(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            print('token: ', token)
            try:
                # print('getting payload')
                payload = verify_decode_jwt(token)
            except:
                abort(401)

            print('checking permissions')
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth


# @app.route('/login', methods=['GET'])
# def login_user():
#     return redirect('https://the-football-pool.eu.auth0.com/authorize?audience=fbpool&response_type=token&client_id=0iNaLqH6uT9Q22PSgTKgnz8Lv7d1N5T7&redirect_uri=https://localhost://5000/login-result')


@app.route('/', methods=['GET'])
def home_page():
    return 'welcome !'


@app.route('/picks', methods=['GET'])
@requires_auth_permission('post:pics')
def submit_picks(permission):
    # unpack request header
    return 'submit your picks'
