import leveldb
import json

db = leveldb.LevelDB('./algolia')


def complete_thread():
    """ Validates that every item in the database is complete (no item in 
    the database that could not find a parant)."""

    for k, v in db.RangeIter():
        json_obj = json.loads(v)
        if 'parent_id' in json_obj:
            parent_id = json_obj['parent_id']
        else:
            parent_id = None

        if parent_id != None:
            try:
                db.Get(str(parent_id))
                parent_exist = True
            except KeyError:
                parent_exist = False
            #print parent_exist
            if not parent_exist:
                print k, parent_id
                #print 'fucked' + '!' * 50



def get_urls():
    for k, v in db.RangeIter():
        obj = json.loads(v)
        if 'url' in obj and obj['url'] != '':
            yield obj['url']

if __name__ == '__main__':
    urls = list(get_urls())
    for url in urls:
        print url
    print len(urls)

