import shelve

from web_app import constant, errors


class Dao:

    def __init__(self, db_path):
        self.db_path = db_path

        # Init db
        with shelve.open(constant.SHELVE_FILENAME, 'n') as db:
            db['init'] = True

    def retrieve(self, key):
        if not self._exists(key):
            raise errors.NotFoundError(f'"{key}" not found in database.')

        with shelve.open(self.db_path, 'r') as db:
            return db[key]

    def update(self, key, new_value):
        if not self._exists(key):
            raise errors.NotFoundError(f'"{key}" not found in database.')

        with shelve.open(self.db_path, 'c') as db:
            db[key] = new_value

    def create(self, key, value):
        if self._exists(key):
            raise errors.AlreadyExists(f'"{key}" already exists in database.')

        with shelve.open(self.db_path, 'c') as db:
            db[key] = value

    def delete(self, key):
        if not self._exists(key):
            raise errors.NotFoundError(f'"{key}" not found in database.')

        with shelve.open(self.db_path, 'c') as db:
            del db[key]

    def _exists(self, key):
        with shelve.open(self.db_path, 'r') as db:
            return key in db
