import configparser
import json

from peewee import *


db = MySQLDatabase('boss', user="root", password="123456", port=3306, host='localhost')


class Jobs(Model):
    id_job = TextField()
    url = TextField()
    company_name = CharField()
    salary = CharField()
    scale = CharField()
    job_name = CharField()
    hr = CharField()
    chated = IdentityField()
    active = IntegerField()
    region = CharField()

    class Meta:
        database = db


db.create_tables([Jobs])
