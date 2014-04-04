#_*_　coding:utf-8 _*_

#http://www.cnblogs.com/coser/archive/2011/12/14/2287739.html

import json

if __name__ == "__main__":
	result = json.loads('{"a":"2", "b":"3", "c":["http://123", "http://234"], "d":"sfeasfea"}')
	print type(result)
	print result