#encoding:utf-8
import app.config
from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
app=Flask(__name__)
app.config.from_object(config)
db.init_app(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")