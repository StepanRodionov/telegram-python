# -*- coding: utf-8 -*-

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

from lib.bot import Bot
import settings.settings as settings
import urllib3
urllib3.disable_warnings()


bot = Bot(token=settings.token())