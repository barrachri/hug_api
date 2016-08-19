# Stdlib imports
import datetime
from functools import wraps
# 3rd party lib imports
from peewee import *

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    """Users model"""
    email = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    blog = CharField()
    password = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('email',)
