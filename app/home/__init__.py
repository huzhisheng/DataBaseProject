from flask import Blueprint

home = Blueprint("home", __name__)

# 必须要import
import app.home.web
