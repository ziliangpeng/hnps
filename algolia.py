from urllib2 import urlopen
import json

URL_PATTERN = 'http://hn.algolia.com/api/v1/items/%d'


def save(item_id, json_object):
    pass

def parse(json_object):
    item_id = json_object['id']

    obj_cnt = 1
    for child in json_object['children']:
        obj_cnt += parse(child)

    save(item_id, json_object)
    return obj_cnt


def is_exist(item_id):
    pass


total_found = 0
for i in range(1, 10):
    print 'item', i,
    if is_exist(i):
        print 'existed',
    else:
        url = URL_PATTERN % i
        try:
            raw_json = urlopen(url).read()
            json_object = json.loads(raw_json)
            item_cnt = parse(json_object)
            print item_cnt, 'found',
            total_found += item_cnt
            print 'total found:', total_found,
        except Exception as e:
            print e,

    print ''

