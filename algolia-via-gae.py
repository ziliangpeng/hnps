from urllib2 import urlopen
import json
import leveldb

URL_PATTERN = 'http://proxy-lord.appspot.com/?item=%d'

db = leveldb.LevelDB('./algolia')
error_items = leveldb.LevelDB('./error_items')
IGNORE_error = True


def save(item_id, json_object):
    db.Put(str(item_id), json.dumps(json_object))


def parse(json_object):
    item_id = json_object['id']

    obj_cnt = 1
    for child in json_object['children']:
        obj_cnt += parse(child)

    save(item_id, json_object)
    return obj_cnt


def is_exist(item_id):
    try:
        db.Get(str(item_id))
        return True
    except KeyError:
        return False


def is_error(item_id):
    try:
        error_items.Get(str(item_id))
        return True
    except KeyError:
        return False


total_found = 0
for i in range(3000000, 7000000):
    if is_exist(i):
        #print 'existed',
        total_found += 1
    elif IGNORE_error and is_error(i):
        #print 'was error',
	pass
    else:
	print 'item', i,
        url = URL_PATTERN % i
        try:
            raw_json = urlopen(url).read()
            json_object = json.loads(raw_json)
            item_cnt = parse(json_object)
            print item_cnt, 'found',
            total_found += item_cnt
            print 'total found:', total_found,
        except Exception as e:
            error_items.Put(str(i), str(e))
            print str(e),

	print ''

