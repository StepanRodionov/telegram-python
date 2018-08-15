# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

class Common:

    def __init__(self):
        pass

    @staticmethod
    def debprint(text, mode='default', file=False):
        try:
            if file:
                fl = open('log.txt', 'a')
                fl.write(text + '\n')
                fl.close()
            else:
                print(text, mode);
        except Exception as e:
            print(e)