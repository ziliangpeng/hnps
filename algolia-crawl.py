from urllib2 import urlopen, HTTPError
import json
import leveldb
from threading import Lock, Thread
from Queue import Queue, Empty
import random
import algolia_io
import sys


URL_PATTERN1 = 'http://proxy-lord.appspot.com/?item=%d'
URL_PATTERN2 = 'http://hnps-ips.appspot.com/?item=%d'

URLS = [URL_PATTERN1, URL_PATTERN2]

IGNORE_error = True
lock = Lock()

engine = algolia_io.LevelDBStorage()


def parse(json_object):
    item_id = json_object['id']

    obj_cnt = 1
    for child in json_object['children']:
        obj_cnt += parse(child)

    def retrieve_id(d):
        return d['id']

    def transform_obj(obj):
        obj['children'] = map(retrieve_id, obj['children'])

    if len(json_object['children']) > 0 and type(json_object['children'][0]) not in (int, long):
        transform_obj(json_object)
    engine.add_post(str(item_id), json_object)
    return obj_cnt


q = Queue()
START = int(sys.argv[1]) #3000000 - 10
COUNT = int(sys.argv[2]) #2000000
for i in range(START, START + COUNT):
    q.put(i)


total_found = 0
stopped = False


def log_error(key, value, save_to_db):
    if save_to_db:
        engine.add_error(str(key), str(value))
    with lock:
        print 'item', key,
        print str(value)


def crawl():
    global total_found
    global stopped
    global URLS
    while True:
        if stopped:
            break
        try:
            i = q.get_nowait()
        except Empty:
            break

        if engine.is_post(str(i)):
            #print 'existed',
            total_found += 1
        elif engine.is_poll(str(i)):
            total_found += 1
        elif IGNORE_error and engine.is_error(str(i)):
            #print 'was error',
            pass
        else:
            URL_PATTERN = random.choice(URLS)
            url = URL_PATTERN % i
            try:
                raw_json = urlopen(url).read()
                json_object = json.loads(raw_json)
                if json_object['type'] in ('poll', 'pollopt'):
                    engine.add_poll(str(i), json_object)
                    with lock:
                        print 'item', i, 'is poll'
                        total_found += 1
                else:
                    item_cnt = parse(json_object)
                    with lock:
                        print 'item', i,
                        print '%3d' % item_cnt, 'found',
                        total_found += item_cnt
                        print 'total found:', total_found
            except HTTPError as e:
                if e.code / 100 == 5: # 5xx Server Error
                    log_error(i, e, False)
                elif e.code == 403: # 403 Permission Denied - banned
                    log_error(i, e, False)
                else:
                    log_error(i, e, True)
            except Exception as e:
                log_error(i, e, False)


def main():
    NUM_OF_THREAD = 9
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

