# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

from telegram.ext import Updater         # пакет называется python-telegram-bot, но Python-
from telegram.ext import Filters         # пакет называется python-telegram-bot, но Python-
from telegram.ext import CommandHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯
from telegram.ext import MessageHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯
import telegram
import requests
import json
import re

from lib.user import User
from lib.dbconn import *


class Bot:

    def __init__(self, token):
        self.need_update = False
        self.updater = Updater(token=token)
        self.addHandlers()
        self.updater.start_polling(clean=True)
        self.updater.idle()

    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

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

        loc_handler = MessageHandler(Filters.location, self.location)
        self.updater.dispatcher.add_handler(loc_handler)
        
        # todo - добавить полезных команд

    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Привет! Чем могу быть полезен?")

    def message(self, bot, update):
        mestext = update.message.text
        command = mestext.lower()
        if command == 'reload':
            self.need_update = True
            return
        elif re.sub(r'[^\w\s]', '', command) == 'где я':
            try:
                kbutts = [
                    telegram.KeyboardButton('Узнать адрес', request_location=True)
                ]
                reply_markup = telegram.ReplyKeyboardMarkup(self.build_menu(kbutts, n_cols=1), resize_keyboard=True,
                                                            one_time_keyboard=True)
                bot.send_message(update.message.chat_id, "Нажмите кнопку", reply_markup=reply_markup)
            except Exception as e:
                self.debprint(e, 'mess_geo')
                bot.sendMessage(chat_id=update.message.chat_id, text='Ошибка!')
            return
        else:
            text = 'Текст вашего сообщения - ' + mestext
            bot.sendMessage(chat_id=update.message.chat_id, text=text)


    def help(self, bot, update):
        text = '''
/start - начинает работу с ботом (необязательна)
/help - список доступных команд
/geo - возвращает список сервисов связанных с геопозиционированием
/reg [имя][фамилия][отчество] - регистрация пользователя (позволит боту отсылать уведомления)
        '''
        bot.sendMessage(chat_id=update.message.chat_id, text=text)

    def geo(self, bot, update):
        # TODO - переделать по обычную клавиатуру
        # TODO №2 - вынести генерацию кнопок в класс butt_generator, а действие в функцию request_geopoint
        # TODO №3 - добавить кнопку на прогноз погоды в текущем месте (собрать несколько источников и выдать красивую сводку)
        try:
            kbutts = [
                telegram.KeyboardButton('Где я?', request_location=True)
            ]
            reply_markup = telegram.ReplyKeyboardMarkup(self.build_menu(kbutts, n_cols=1), resize_keyboard=True, one_time_keyboard=True)
            bot.send_message(update.message.chat_id, "Выберите действие", reply_markup=reply_markup)
        except Exception as e:
            print(e)
            bot.sendMessage(chat_id=update.message.chat_id, text='Ошибка!')

    def location(self, bot, update):
        loc = update.message.location
        yandex_url = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode=' + str(loc.longitude) + ', ' + str(loc.latitude)
        resp = requests.get(yandex_url)
        txt = resp.text
        jsn = json.loads(txt)
        try:
            addr = jsn['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        except Exception as e:
            addr = 'Не удалось установить адрес! Попробуйте еще раз'

        bot.sendMessage(chat_id=update.message.chat_id, text=addr)


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
