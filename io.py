import leveldb


class StorageOption:

    def get(key):
        raise NotImplementedError()

    def add_post(key, value):
        raise NotImplementedError()

    def add_poll(key, value):
        raise NotImplementedError()

    def add_error(key, error_message):
        raise NotImplementedError()

    def is_poll(key):
        raise NotImplementedError()

    def is_error(key):
        raise NotImplementedError()

    def is_post(key):
        raise NotImplementedError()

    def exists(key):
        return is_post(key) or is_error(key) or is_poll(key)


class LevelDBStorage(StorageOption):

    POST_DATA_DIR = 'algolia'
    POLL_DIR = 'polls'
    ERRORS_DIR = 'error_items'

    def __init__(self):
        self.data_db = leveldb.LevelDB(POST_DATA_DIR)
        self.poll_db = leveldb.LevelDB(POLL_DIR)
        self.error_db = leveldb.LevelDB(ERRORS_DIR)

    def get(self, key):
        if self.is_post(key):
            return self.data_db.Get(key)
        elif self.is_poll(key):
            return self.poll_db.Get(key)
        elif self.is_error(key):
            return self.error_db.Get(key)
        else:
            raise KeyError()

    def __add_to_db_func(db):
        def add_tp(key, value):
            db.Put(key, value)

    add_post = __add_to_db_func(self.data_db)
    add_poll = __add_to_db_func(self.poll_db)
    add_error = __add_to_db_func(self.error_db)

    def __in_db_func(db):
        def is_in(key):
            try:
                db.Get(key)
                return True
            except KeyError:
                return False

    is_post = __in_db_func(self.data_db)
    is_poll = __in_db_func(self.poll_db)
    is_error = __in_db_func(self.error_db)


