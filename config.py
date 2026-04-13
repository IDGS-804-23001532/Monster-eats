from re import DEBUG
import os

from sqlalchemy import create_engine

class Config():
    SECRET_KEY = "ClaveSecreta"

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Gerente:Moster&EatsDUCA$@localhost/monster_eats_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'monstereatsmail@gmail.com'
    MAIL_PASSWORD = 'xtuyovvivveypura'

