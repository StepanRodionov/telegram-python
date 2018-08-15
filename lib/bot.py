# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

from telegram.ext import Updater         # пакет называется python-telegram-bot, но Python-
from telegram.ext import Filters         # пакет называется python-telegram-bot, но Python-
from telegram.ext import CommandHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯
from telegram.ext import MessageHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯

from lib.user import User
from lib.dbconn import *


class Bot:

    def __init__(self, token):
        self.updater = Updater(token=token)
        self.addHandlers()
        self.updater.start_polling(clean=True)
        self.updater.idle()

    def addHandlers(self):
        start_handler = CommandHandler('start', self.start)
        self.updater.dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.help)
        self.updater.dispatcher.add_handler(help_handler)

        geo_handler = CommandHandler('geo', self.geo)
        self.updater.dispatcher.add_handler(geo_handler)

        reg_handler = CommandHandler('reg', self.reg)
        self.updater.dispatcher.add_handler(reg_handler)

        text_handler = MessageHandler(Filters.text, self.message)
        self.updater.dispatcher.add_handler(text_handler)

    def start(self, bot, update):
        self.debprint(str(update.message.chat_id), 'start');
        bot.sendMessage(chat_id=update.message.chat_id, text="Привет! Чем могу быть полезен?")

    def message(self, bot, update):
        mestext = update.message.text
        self.debprint(mestext, 'mess');
        try:
            text = 'Текст вашего сообщения - ' + mestext
            bot.sendMessage(chat_id=update.message.chat_id, text=text)
        except Exception as e:
            print(e)
            bot.sendMessage(chat_id=update.message.chat_id, text='Ошибка!')

    def help(self, bot, update):
        text = '''
/start - начинает работу с ботом (необязательна)
/help - список доступных команд
/geo - возвращает список сервисов связанных с геопозиционированием
/reg [имя][фамилия][отчество] - регистрация пользователя (позволит боту отсылать уведомления)
        '''
        bot.sendMessage(chat_id=update.message.chat_id, text=text)

    def geo(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text='TODO')

    def reg(self, bot, update):
        text = 'Что-то пошло не так...'
        try:
            mestext = update.message.text
            args = mestext.split(' ')[1:]
            user = User.getName(args)
            print(user)
            try:
                p = Person()
                #usertable.create(chat_id=update.message.chat_id, name=user['name'], surname=user['surname'], patronymic=user['patronymic'])
                text = p.create(chat_id=update.message.chat_id, name=user['name'], surname=user['surname'], patronymic=user['patronymic'])
            except Exception as e:
                self.debprint('Error in DB ' + str(e))
                text = 'Ошибка в БД'
        except Exception as e:
            self.debprint(e, '', True)
            text = 'Ошибка при обработке данных'
        finally:
            bot.sendMessage(chat_id=update.message.chat_id, text=text)

    def debprint(self, text, mode='default', file=False):
        CO.debprint(text, mode, file)