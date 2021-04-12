#encoding:utf-8

from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory
from app.models import like_relation_table
from app.models import UserInfo,ImgInfo,VideoInfo,ReviewInfo,MsgInfo,StarInfo,WatchRelation,StarRelation,FansRelation,AdminInfo
from . import admin
from app import app,db
from app.decorators import admin_required
from datetime import datetime
from sqlalchemy import and_,or_
import os

# 首页函数
@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


# 登录函数
@admin.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('admin/login.html')
    else:
        account = request.form.get('admin_account')
        password = request.form.get('admin_password')
        
        # 在数据库中查找账号和密码是否对应
        admin = AdminInfo.query.filter(AdminInfo.admin_account == account, AdminInfo.admin_pass == password).first()

        # 如果正确
        if admin:
            session['admin_id']=admin.admin_id
            # 如果想在31天内都不需要登录
            session.permanent=True
            # 登录成功跳转到首页
            return redirect(url_for('admin.index'))
        else:
            return u'账号或者密码错误，请确认后再登录！'

# 注销函数
@admin.route('/logout/')
def logout():
    # 删除cookie
    # session.pop('user_id')
    del session['admin_id']
    # 删除所有cookie
    # session.clear()
    return redirect(url_for('admin.login'))

# 查看用户列表
@admin.route('/manage_user/')
@admin_required
def manage_user():
    return render_template('admin/manage_user.html', user_list = UserInfo.query.all())

# 删除一位用户
@admin.route('/delete_user/')
@admin_required
def delete_user():
    user_id = request.args.get('user_id')
    user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.manage_user'))

# 查看视频列表
@admin.route('/manage_video/')
@admin_required
def manage_video():
    return render_template('admin/manage_video.html', video_list = VideoInfo.query.all())

# 删除一个视频
@admin.route('/delete_video/')
@admin_required
def delete_video():
    video_id = request.args.get('video_id')
    video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('admin.manage_video'))

# 查看图片列表
@admin.route('/manage_img/')
@admin_required
def manage_img():
    return render_template('admin/manage_img.html', img_list = ImgInfo.query.all())

# 删除一个图片
@admin.route('/delete_img/')
@admin_required
def delete_img():
    img_id = request.args.get('img_id')
    img = ImgInfo.query.filter(ImgInfo.img_id == img_id).first()
    db.session.delete(img)
    db.session.commit()
    return redirect(url_for('admin.manage_img'))