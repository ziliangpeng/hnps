import leveldb
import json


class StorageOption:

    def get(self, key):
        raise NotImplementedError()

    def add_post(self, key, value): # add the json object, not stringified json
        raise NotImplementedError()

    def add_poll(self, key, value): # add the json object, not stringified json
        raise NotImplementedError()

    def add_error(self, key, error_message): # add the json object, not stringified json
        raise NotImplementedError()

    def is_poll(self, key):
        raise NotImplementedError()

    def is_error(self, key):
        raise NotImplementedError()

    def is_post(self, key):
        raise NotImplementedError()

    def exists(self, key):
        return self.is_post(key) or self.is_error(key) or self.is_poll(key)


class LevelDBStorage(StorageOption):

    _DEFAULT_POST_DATA_DIR = 'algolia'
    _DEFAULT_POLL_DIR = 'polls'
    _DEFAULT_ERRORS_DIR = 'error_items'

    def __init__(self,
            POST_DATA_DIR=_DEFAULT_POST_DATA_DIR,
            POLL_DIR=_DEFAULT_POLL_DIR,
            ERRORS_DIR=_DEFAULT_ERRORS_DIR):
        self.data_db = leveldb.LevelDB(POST_DATA_DIR)
        self.poll_db = leveldb.LevelDB(POLL_DIR)
        self.error_db = leveldb.LevelDB(ERRORS_DIR)

        def _add_to_db_func(db):
            def add_tp(key, value):
                stringified = json.dumps(value)
                db.Put(key, stringified)
            return add_tp

        def _in_db_func(db):
            def is_in(key):
                try:
                    db.Get(key)
                    return True
                except KeyError:
                    return False
            return is_in

        self.add_post = _add_to_db_func(self.data_db)
        self.add_poll = _add_to_db_func(self.poll_db)
        self.add_error = _add_to_db_func(self.error_db)

        self.is_post = _in_db_func(self.data_db)
        self.is_poll = _in_db_func(self.poll_db)
        self.is_error = _in_db_func(self.error_db)


    def get(self, key):
        def _load_json_obj(db, key):
            value = db.Get(key)
            return json.loads(value)

        if self.is_post(key):
            return _load_json_obj(self.data_db, key)
        elif self.is_poll(key):
            return _load_json_obj(self.poll_db, key)
        elif self.is_error(key):
            return _load_json_obj(self.error_db, key)
        else:
            raise KeyError()




