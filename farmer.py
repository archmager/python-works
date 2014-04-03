#_*_ coding: utf-8 _*_
import urllib
from HTMLParser import HTMLParser
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)

class PageParser(HTMLParser):
	"""parse a page"""
	def __init__(self, url):
		self.content=[]
		self.urlMap={}
		self.atag=0
		self.tmpUrl=''
		self.tmpContent=''
		self.url = url
		HTMLParser.__init__(self)
	def handle_starttag(self,tag,attrs):
		if tag == 'a':
			self.atag = 1
			for name,value in attrs:
				if name == 'href':
					self.tmpUrl = self.url + value
	def handle_endtag(self, tag):
		if tag == 'a':
			self.atag = 0
        	self.content.append(self.tmpContent)
        	self.urlMap[self.tmpContent] = self.tmpUrl
	def handle_data(self, data):
		if self.atag:
			self.tmpContent = data.decode("GBK") 
	def getUrlMap(self):
		return self.urlMap
	def getResult(self, keyword):
		resultMap={}
		for (k,v) in self.urlMap.items():
			print k
			if k.find(keyword) > 0:
				resultMap[k] = v
		return resultMap


class UrlCreator(object):
	"""create urls by conditions"""
	def createUrl(self, keyword, time, page):
		return ["http://67.220.91.20/bbs/forum-230-%s.html" % (x) for x in xrange(1,int(page)+1)]

class UrlPaser(object):
	"""download and parse"""
	def __init__(self):
		self.resultMap={}
	def parseUrl(self, urls, keyword):
		for url in urls:
			#content = urllib.urlretrieve(url, "/tmp/"+url.split('/')[-1])
			pp = PageParser("http://67.220.91.20/bbs/")
      		pp.feed(urllib.urlopen(url).read())
      		pp.close()
      		for (k,v) in pp.getResult(keyword).items():
      			self.resultMap[k]=v
		return self.resultMap

		
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
		return up.parseUrl(urls, self.keyword)



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_argument('keyword', '')
        time = self.get_argument('time', '2000-01-01')
        page = self.get_argument('page', '100')
        self.write(keyword + ' ' + time + ' ' + page) 
        sf = SupriseFinder(keyword, time, page)
        for (k, v) in sf.findSuprise().items():
        	self.write("<a href=\"" + v + "\">" + k + "</a><br />")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()