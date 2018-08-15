# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

class User:

    def __init__(self):
        pass

    @staticmethod
    def getName(args):
        name = None; surname = None; patr = None;
        try:
            name = args.pop(0)
            surname = args.pop(0)
            patr = args.pop(0)
        except IndexError:
            pass
        finally:
            return {'name': name, 'surname': surname, 'patronymic': patr}
