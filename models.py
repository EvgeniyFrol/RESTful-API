from datetime import datetime

from peewee import Model, CharField, SqliteDatabase, ForeignKeyField, DateTimeField

db = SqliteDatabase('base.db')


class User(Model):
    username = CharField(unique=True)
    password = CharField()
    avatar = CharField()
    phone_number = CharField()

    class Meta:
        database = db


class Message(Model):
    sender = ForeignKeyField(User, backref='sent_messages')
    content = CharField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([User, Message])
