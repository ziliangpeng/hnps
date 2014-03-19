from urllib2 import urlopen
import json
import leveldb
from threading import Lock, Thread
from Queue import Queue


db = leveldb.LevelDB('./algolia')
db2 = leveldb.LevelDB('./reduced_db')


def main():
    def retrieve_id(d):
        return d['id']

    def reduce_item(obj):
        if 'children' in obj and len(obj['children']) > 0:
            if type(obj['children'][0]) not in (int, long):
                obj['children'] = map(retrieve_id, obj['children'])
            
        return obj

    for k, v in db.RangeIter():
        v = json.loads(v)
        v = reduce_item(v)
        v = json.dumps(v)
        db2.Put(k, v)


if __name__ == '__main__':
    main()

