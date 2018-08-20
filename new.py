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


bot = lib.bot.Bot(token=settings.token())

# set_interval(reloader, 5, bot)                TODO - автоперезагрузка!
