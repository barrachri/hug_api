import datetime
from functools import wraps
from peewee import *

db = SqliteDatabase(None)

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = db

# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel):
    email = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    blog = CharField()
    password = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('email',)
