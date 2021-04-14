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
@admin.route('/manage_user/', methods = ['GET', 'POST'])
@admin_required
def manage_user():
    if request.method == 'GET':
        return render_template('admin/manage_user.html', user_list = UserInfo.query.all())
    else:
        # 修改一位用户
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        user_pass = request.form.get('user_pass')
        user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
        user.user_name = user_name
        user.user_pass = user_pass
        db.session.commit()
        return render_template('admin/manage_user.html', user_list = UserInfo.query.all())





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
    img_list = ImgInfo.query.all()
    for img in img_list:
        if img.img_video:
            print(img.img_video[0].video_title)
    return render_template('admin/manage_img.html', img_list = img_list)

# 查看视频评论列表
@admin.route('/manage_review/')
@admin_required
def manage_review():
    return render_template('admin/manage_review.html', review_list = ReviewInfo.query.all())

# 删除一个视频评论
@admin.route('/delete_review/')
@admin_required
def delete_review():
    review_id = request.args.get('review_id')
    review = ReviewInfo.query.filter(ReviewInfo.review_id == review_id).first()
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('admin.manage_review'))

# 查看消息列表
@admin.route('/manage_msg/')
@admin_required
def manage_msg():
    return render_template('admin/manage_msg.html', msg_list = MsgInfo.query.all())

# 删除一条消息
@admin.route('/delete_msg/')
@admin_required
def delete_msg():
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    msg_time = request.args.get('msg_time')
    msg = MsgInfo.query.filter(MsgInfo.sender_id==sender_id, MsgInfo.receiver_id==receiver_id, MsgInfo.msg_time==msg_time).first()
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for('admin.manage_msg'))

