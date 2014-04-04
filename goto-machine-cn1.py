#_*_　coding:utf-8 _*_

import sys
import os


if __name__ == "__main__":
	goto = sys.argv[1]
	print goto
	pofix = {"tw" : "l-ttstw%s.f.beta.cn6", "n" : "l-ttsn%s.f.dev.cn6", "test" : "l-ttstest%s.f.beta.cn6"}
	for (k, v) in pofix.items():
		print k
		print v
		if goto.find(k) >= 0:
			num = goto.replace(k, "")
			print v % (num)
			os.system("ssh " + v % (num))

