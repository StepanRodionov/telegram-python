# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import settings.settings as settings
from peewee import *
from lib.common import Common as CO

db = MySQLDatabase(settings.dbname, user=settings.dbuser, passwd=settings.dbpasswd, host=settings.dbhost)


class usertable(Model):

    id = IntegerField()
    chat_id = CharField()
    name = CharField()
    surname = CharField()
    patronymic = CharField()
    email = CharField()
    phone = CharField()

    class Meta:
        database = db
        db_table = 'users'


class Person:

    def create(self, **kwargs):
        chat_id = kwargs['chat_id']
        try:
            ps = usertable.select().where(usertable.chat_id == chat_id).get()
            print(ps)
            return 'Вы уже зарегистированы'
        except Exception:
            CO.debprint(kwargs, '', True)
            name = kwargs['name'] if 'name' in kwargs else ''
            surname = kwargs['surname'] if 'surname' in kwargs else ''
            patronymic = kwargs['patronymic'] if 'patronymic' in kwargs else ''
            usertable.create(chat_id=chat_id, name=name, surname=surname, patronymic=patronymic)
            return 'Вы успешно зарегистрированы!'

