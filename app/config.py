# to get a string like this run:
# openssl rand -hex 32
from os import environ


class Settings:
    SECRET_KEY = environ["SECRET_KEY"]
    ALGORITHM = environ["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = int(environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    DB_NAME = environ["DB_NAME"]
    DB_PASSWORD = environ["DB_PASSWORD"]
    DB_HOST_NAME = environ["DB_HOST_NAME"]
    DB_PORT = environ["DB_PORT"]
    DB_USER = environ["DB_USER"]
