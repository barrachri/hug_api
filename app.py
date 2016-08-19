"""A simple project about API with HUG"""

# Stdlib imports
import os
from functools import wraps
# 3rd party lib imports
import hug
import peewee
# Local imports
import settings
from models import db, User
from utils import Token

# Handling database creation
if settings.TESTING:
    db.init(settings.TEST_APP_DB)
    db.connect()
    db.create_tables([User])
    db.close()
else:
    if not os.path.exists(settings.APP_DB):
        db.init(settings.APP_DB)
        db.connect()
        db.create_tables([User])
        db.close()
    else:
        db.init(settings.APP_DB)

hug_api = hug.API(__name__)
@hug.request_middleware(api=hug_api)
def process_data(request, response):
    db.connect()

@hug.response_middleware(api=hug_api)
def process_data(request, response, resource):
    db.close()



# API format
success = {"data" : {}}
error = { "code": None, "message": None }

# Token generation
token = Token(settings.KEY)
token_key_authentication = hug.authentication.token(token)
login_required = hug.http(requires=token_key_authentication)


@hug.post("/users/create", versions=1)
def create_user(email: hug.types.text, password: hug.types.text,
                first_name: hug.types.text, last_name: hug.types.text,
                blog: hug.types.text, response=None):
    """This api creates a new user"""
    try:
        user = User.create(email=email, password=password,
                            first_name=first_name, last_name=last_name,
                            blog=blog)
    except peewee.IntegrityError as err:
        error['code'] = 400
        error['message'] = "{}".format(err)
        response.status = hug.HTTP_400
        return {"error": error}
    success['data'] = { "code": 200, "message": 'User {0} created'.format(user.email)}
    return success

@hug.get("/users/login", versions=1)
def login_user(email: hug.types.text, password: hug.types.text, response=None):
    """This api returns a token given a valid email and password"""
    try:
        user = User.get(User.email == email and User.password == password)
        user_token = token.create(user.id)
        success['data'] = {"token": user_token}
        return success
    except User.DoesNotExist:
        error['code'] = 400
        error['message'] = "User does not exist"
        response.status = hug.HTTP_400
        return {"error": error}

@login_required.get("/users", versions=1)
def get_info_user(token: hug.directives.user):
    """This api returns returns a info about the user"""

    user = User.get(User.id == token['user_id'])
    success['data'] = user.__dict__["_data"]
    return success

@login_required.put("/users", versions=1)
def update_info_user(token: hug.directives.user, first_name=None, last_name=None, blog=None, password=None):
    """This api updates the info about the user"""

    user = User.get(User.id == token['user_id'])
    data = locals().copy()
    fields = ["first_name", "last_name", "blog", "password"]
    for k,v in data.items():
        if k in fields and v is not None:
            user.__setattr__(k, v)
    user.save()

    success['data'] = user.__dict__["_data"]
    return success
