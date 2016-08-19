# Stdlib imports
from os import urandom
from base64 import urlsafe_b64encode
from datetime import datetime, timedelta
from functools import wraps
# 3rd party lib imports
import jwt
from itsdangerous import URLSafeTimedSerializer, BadSignature

class Token():
    """Class to create and verify tokens"""
    def __init__(self, key):
        self.key = key
    def create(self, id, expire=30):
        """This function returns a JWT token with the user_id, expired time and uuid (jti)
        """
        token_generated = datetime.utcnow()
        token_expire = datetime.utcnow() + timedelta(minutes=expire)
        jti = urlsafe_b64encode(urandom(16))
        payload = {'user_id': id, 'iat': token_generated, 'exp': token_expire}
        token = jwt.encode(payload, self.key, "HS512")
        return token

    def __call__(self, token):
        """This function verifies if the given token is still valid"""
        try:
            if token is None:
                return None
            return jwt.decode(token, self.key)
        except (jwt.ExpiredSignature, jwt.DecodeError) as e:
            return False
