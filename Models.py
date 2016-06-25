"""
The `Models.py` file is where all models are held.

This may be changed in the future so models are
contained in their own file and or directory,
but as of now, they must be in Models.py.
"""

import datetime
from Config.Environment import env, get_database
from peewee import *

db = get_database(env("DB_TYPE"))


class BaseModel(Model):
    class Meta:
        database = db


# The User model stores passwords for retrieval in case you need
# to log in to a website.  It is not meant to store passwords
# securely, but this can be accomplished by modifying the
# `Middleware/UserMiddleware.py` file if it is needed.
class User(BaseModel):
    """ The basic User model """

    username = CharField()
    email = CharField()
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
