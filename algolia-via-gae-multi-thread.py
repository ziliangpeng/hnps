from urllib2 import urlopen, HTTPError
import json
import leveldb
from threading import Lock, Thread
from Queue import Queue
import random


URL_PATTERN1 = 'http://proxy-lord.appspot.com/?item=%d'
URL_PATTERN2 = 'http://hnps-ips.appspot.com/?item=%d'

URLS = [URL_PATTERN1, URL_PATTERN2]


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


import sys
q = Queue()
START = int(sys.argv[1]) #3000000 - 10
COUNT = int(sys.argv[2]) #2000000
for i in range(START, START + COUNT):
    q.put(i)


total_found = 0
stopped = False


def log_error(key, value):
    error_items.Put(str(key), str(value))
    with lock:
        print 'item', key,
        print str(value)


def crawl():
    global total_found
    global stopped
    global URLS
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
            URL_PATTERN = random.choice(URLS)
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
            except HTTPError as e:
                if e.code != 403:
                    log_error(i, e)
            except Exception as e:
                log_error(i, e)


def main():
    NUM_OF_THREAD = 4
    threads = []
    for i in range(NUM_OF_THREAD):
        thread = Thread(target = crawl)
        thread.start()
        threads.append(thread)

    global stopped
    #raw_input()
    #stopped = True

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()

