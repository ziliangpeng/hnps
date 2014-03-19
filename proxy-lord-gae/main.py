import os
import datetime
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users

import urllib2
import urlparse

ROUTE_DOMAIN = 'http://hn.algolia.com/api/v1/items/'

class StartPage(webapp.RequestHandler):

    def get(self):
        qs = self.request.query_string
        queries = urlparse.parse_qs(qs)
        if 'item' not in queries or len(queries['item']) != 1:
            self.response.set_status(400, 'query string should include 1 item')
        else:
            item_id = queries['item'][0]

            route_url = ROUTE_DOMAIN + str(item_id)
            headers={'User-Agent' : 'NetBee. Contact me: ziliang.me@gmail.com'}
            req = urllib2.Request(url=route_url, headers=headers)
            try:
                raw_json = urllib2.urlopen(req).read()
                self.response.headers['Content-Type'] = "application/json"
                self.response.out.write(raw_json)
            except urllib2.HTTPError as e:
                self.response.set_status(e.code, e.reason)
            except Exception as e:
                Response.http_status_message(500)


application = webapp.WSGIApplication([('/.*', StartPage)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
