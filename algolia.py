from urllib2 import urlopen

URL_PATTERN = 'http://hn.algolia.com/api/v1/items/%d'


for i in range(1, 1000):
    print 'item', i
    url = URL_PATTERN % i
    print url
    try:
        print urlopen(url).read()
    except Exception as e:
        print e

