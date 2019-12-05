import datetime
# import pdb

import jwt
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
SECRET_KEY = os.getenv('SECRET_KEY')
AUTH_ENDPOINT = os.getenv('AUTH_ENDPOINT')


def token_activation(username, password):
    """
    :param username: takes user name as parameter
    :param password: takes password
    :return: will return token
    """

    data = {
        'username': username,
        'password': password,
        'exp': datetime.datetime.now() + datetime.timedelta(days=2)
    }

    token = jwt.encode(data, SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token


def token_validation(username, password):
    """
    :param username: takes user name as parameter
    :param password: takes password
    :return: will return token
    """

    data = {
        'username': username,
        'password': password
    }
    tokson = requests.post(AUTH_ENDPOINT, data=data)
    token = tokson.json()['access']
    return token