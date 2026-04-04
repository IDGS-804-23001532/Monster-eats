from re import DEBUG
import os

from sqlalchemy import create_engine

class Config():
    SECRET_KEY = "ClaveSecreta"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@localhost:3306/monster_eats_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
