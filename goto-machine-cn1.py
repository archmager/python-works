#_*_　coding:utf-8 _*_

import sys
import os


if __name__ == "__main__":
	goto = sys.argv[1]
	print goto
    os.system("ssh l-tts" + goto + ".f.cn1")

