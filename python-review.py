#coding: utf-8

myString = 'hello world'
print myString

#format string
print "%s is a %s" % ('sam', 'coder')

#tranverse list
foo = ['a', 'b', 'c', 'd']
for i, c in enumerate(foo):
	print c, "%d" % i

#列表解析
for i in [x**2 for x in range(1,10) if not x%2]:
	print i