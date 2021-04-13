# 装饰器函数
from functools import wraps
from flask import session,redirect,url_for
from app.models import AdminInfo
from app import db

# 登陆限制装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('home.login'))
    return wrapper

# 登陆限制装饰器
def admin_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('admin_id'):
            return func(*args,**kwargs)
        else:
            # 建立一个默认管理员账户, 账号'root', 密码'root'
            admin = AdminInfo.query.filter(AdminInfo.admin_account=='root').first()
            if admin == None:
                print("admin", admin)
                admin = AdminInfo(admin_account='root', admin_pass='root')
                db.session.add(admin)
                db.session.commit()
            return redirect(url_for('admin.login'))
    return wrapper