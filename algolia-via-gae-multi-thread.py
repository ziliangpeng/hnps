from urllib2 import urlopen
import json
import leveldb
from threading import Lock, Thread
from Queue import Queue


URL_PATTERN = 'http://proxy-lord.appspot.com/?item=%d'
URL_PATTERN = 'http://hnps-ips.appspot.com/?item=%d'


db = leveldb.LevelDB('./algolia')
error_items = leveldb.LevelDB('./error_items')
IGNORE_error = True
lock = Lock()


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


q = Queue()
START=1000000
COUNT=500000
for i in range(START, START + COUNT):
    q.put(i)


total_found = 0
stopped = False

def crawl():
    global total_found
    global stopped
    while not q.empty():
        if stopped:
            break

        i = q.get()
        if is_exist(i):
            #print 'existed',
            total_found += 1
        elif IGNORE_error and is_error(i):
            #print 'was error',
            pass
        else:
            url = URL_PATTERN % i
            try:
                raw_json = urlopen(url).read()
                json_object = json.loads(raw_json)
                item_cnt = parse(json_object)
                with lock:
                    print 'item', i,
                    print '%3d' % item_cnt, 'found',
                    total_found += item_cnt
                    print 'total found:', total_found
            except Exception as e:
                error_items.Put(str(i), str(e))
                with lock:
                    print 'item', i,
                    print str(e)


def main():
    NUM_OF_THREAD = 5
    threads = []
    for i in range(NUM_OF_THREAD):
        thread = Thread(target = crawl)
        thread.start()
        threads.append(thread)

    global stopped
    raw_input()
    stopped = True

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()

