#encoding:utf-8

import os
from os import path
DEBUG=True

SECRET_KEY=os.urandom(24)

# 数据库配置
HOSTNAME='127.0.0.1'
PORT='3306'
DATABASE='tiktok1'
USERNAME='root'
PASSWORD='root'

DB_URI='mysql+mysqlconnector://{}:{}@{}:{}/{}?auth_plugin=mysql_native_password'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=False

VIDEO_UPLOAD_FOLDER = path.abspath(path.dirname(__file__)) + '/static/videos/'
POSTER_UPLOAD_FOLDER = path.abspath(path.dirname(__file__)) + '/static/posters/'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
