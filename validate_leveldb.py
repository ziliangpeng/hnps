import leveldb
import json

db = leveldb.LevelDB('./algolia')


def complete_thread():
    """ Validates that every item in the database is complete (no item in 
    the database that could not find a parant)."""

    for k, v in db.RangeIter():
        json_obj = json.loads(v)
        parent_id = json['parent_id']
        if parent_id != None:
            print k, parent_id,
            try:
                db.Get(str(parent_id))
                parent_exist = True
            except leveldb.KeyError:
                parent_exist = False
            print parent_exist

        

