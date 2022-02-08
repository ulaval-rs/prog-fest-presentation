import shelve
from hashlib import sha256

from . import constant

SCHEMA = {
    'message': None,
}


def init_message():
    with shelve.open(constant.SHELVE_FILENAME, 'n') as db:
        db['message'] = ''


def user_exists(idul: str) -> bool:
    with shelve.open(constant.SHELVE_FILENAME, 'r') as db:
        return idul in db


def make_new_user(idul: str) -> None:
    token = generate_token(idul)

    with shelve.open(constant.SHELVE_FILENAME, 'c') as db:
        db[token] = SCHEMA


def generate_token(idul: str) -> str:
    return sha256(idul.encode()).hexdigest()

