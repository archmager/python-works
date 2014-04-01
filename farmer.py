import urllib
import HTMLParser
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)

class PageParser(HTMLParser):
	"""parse a page"""
	def handle_starttag(self,tag,attrs):
          if tag =='a':
              for name,value in attrs:
                  if name == 'href' and value[0:6] == 'thread':
                      print attrs


class UrlCreator(object):
	"""create urls by conditions"""
	def createUrl(self, keyword, time, page):
		return ["http://67.220.90.21/bbs/forum-58-%s.html" % (x) for x in xrange(1,int(page)+1)]

class UrlPaser(object):
	"""download and parse"""
	def parseUrl(self, urls):
		for url in urls:
			#content = urllib.urlretrieve(url, "/tmp/"+url.split('/')[-1])
			pp = PageParser()
      		pp.feed(urllib.urlopen(url).read())
            pp.handle_starttag()
            pp.close()

		


class SupriseFinder(object):
	"""find interesting link"""
	def __init__(self, keyword, time, page):
		self.keyword = keyword
		self.time = time
		self.page = page
	def findSuprise(self):
		uc = UrlCreator()
		urls = uc.createUrl(self.keyword, self.time, self.page)
		up =UrlPaser()
		up.parseUrl(urls)



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_argument('keyword', '')
        time = self.get_argument('time', '2000-01-01')
        page = self.get_argument('page', '100')
        self.write(keyword + ' ' + time + ' ' + page) 
        sf = SupriseFinder(keyword, time, page)
        sf.findSuprise()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()