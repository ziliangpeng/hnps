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

    def transform_obj(obj):
        obj['children'] = map(retrieve_id, obj['children'])

    def reduce_item(obj):
        if 'children' in obj and len(obj['children']) > 0:
            if type(obj['children'][0]) not in (int, long):
                transform_obj(obj)
            
        return obj

    limit = 0
    cnt = 0
    byte_count = 0
    for k, v in db.RangeIter():
        if limit == 10000:
            cnt += 1
            print cnt, ' * 10000 items', byte_count
            limit = 0
        limit += 1
        #v = json.loads(v)
        #v = reduce_item(v)
        #v = json.dumps(v)
        byte_count += len(v)
        #db2.Put(k, v)


if __name__ == '__main__':
    main()

