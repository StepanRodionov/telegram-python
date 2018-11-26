# -*- coding: utf-8 -*-

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import lib.bot
import settings.settings as settings
import threading
import importlib
import urllib3
urllib3.disable_warnings()


def set_interval(func, sec, *args):
    def func_wrapper():
        set_interval(func, sec, *args)
        func(*args)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def reloader(bot):
    print(bot.need_update)
    if bot.need_update:
        importlib.reload(lib.bot)

if __name__ == '__main__':
    bot = lib.bot.Bot(token=settings.token())

# автоперезагрузку убрал - ею будет заниматься teamcity или деплой скрипт
