from flask import request, abort, _request_ctx_stack
from urllib.request import urlopen
from functools import wraps
from werkzeug import exceptions
from jose import jwt
import json

AUTH0_DOMAIN = 'the-football-pool.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fbpool'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

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
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        print('kid not in header')
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
            print('expired token')
            # exceptions.Unauthorized({
            #     'code': 'token_expired',
            #     'description': 'Token expired.'
            # })
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            print('cliams error')
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            print('except exception?')
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
            try:
                payload = verify_decode_jwt(token)
            except:
                print('except in wrapper')
                abort(401)

            print('checking permissions')
            check_permissions(permission, payload)
            
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth
