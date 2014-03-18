import urllib2
from bs4 import BeautifulSoup
from time import sleep

URL_PATTERN = 'https://news.ycombinator.com/item?id=%d'


def custom_read(url):
    req = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    return urllib2.urlopen(req).read()


FEAT_REQ = 363

def find_end(text, start):
    start += len('item?id=')
    while text[start] in '0123456789':
        start += 1
    return start

item_id = 1
crawled_items = 0
visited = set()

while 1:
    print 'trying', item_id
    if item_id not in visited:
        url = URL_PATTERN % item_id
        found_ids = []
        try:
            raw_html = custom_read(url)
            f = open(str(item_id) + '.htm', 'w')
            f.write(raw_html)
            f.close()
            """
            soup = BeautifulSoup(raw_html)
            for a in soup.find_all("a"):
                print a['href']
            print '--'
            """

            start_idx = 0
            print 'children:',
            while 1:
                idx = raw_html.find('item?id=', start_idx)
                if idx == -1:
                    break
                end = find_end(raw_html, idx)
                found_url = raw_html[idx:end]
                found_id = int(found_url[found_url.find('=')+1:])
                if found_id != FEAT_REQ:
                    print found_id,
                    found_ids.append(found_id)
                    visited.add(found_id)

                start_idx = idx + 10
            print ''
            visited.add(item_id)
        except Exception as e:
            print 'error', e


        crawled_items += 1
        print 'crawled id:', item_id, 'crawl count:', crawled_items,
        print 'visits', len(found_ids), 'visited', len(visited)
        sleep(30)

    item_id += 1
        
