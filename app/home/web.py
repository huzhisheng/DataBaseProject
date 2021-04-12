#encoding:utf-8

from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory
from app.models import like_relation_table
from app.models import UserInfo,ImgInfo,VideoInfo,ReviewInfo,MsgInfo,StarInfo,WatchRelation,StarRelation,FansRelation
from . import home
from app import app,db
from app.decorators import login_required
from datetime import datetime
from sqlalchemy import and_,or_
import os
import time
import random

random.seed(datetime.now())

# 首页函数
@home.route('/')
def index():
    return render_template('home/index.html',videos = VideoInfo.query.all())

# 登录函数
@home.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('home/login.html')
    else:
        account = request.form.get('account')
        password = request.form.get('password')
        
        # 在数据库中查找手机号码和密码是否对应
        user=UserInfo.query.filter(UserInfo.user_account==account, UserInfo.user_pass==password).first()

        # 如果正确
        if user:
            session['user_id']=user.user_id
            # 如果想在31天内都不需要登录
            session.permanent=True
            # 登录成功跳转到首页
            return redirect(url_for('home.index'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'


# 注册函数
@home.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return render_template('home/regist.html')
    else:
        name = request.form.get('name')
        account = request.form.get('account')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证 如果被注册了 就不能够再次注册
        user=UserInfo.query.filter(UserInfo.user_account==account).first()
        if user:
            return u'该账号已被注册!'
        else:
            # password1和password2相等才可以
            if password1 != password2:
                return u'两次密码不相等，请核对后再次填写!'
            else:
                #可以进行注册
                user=UserInfo(user_name=name,user_account=account,user_pass=password1,user_date=datetime.now())
                # 添加到数据库中
                db.session.add(user)
                # 进行事务提交
                db.session.commit()
                # 如果注册成功，页面跳转到登录界面
                return redirect(url_for('home.login'))


# 注销函数
@home.route('/logout/')
def logout():
    # 删除cookie
    # session.pop('user_id')
    del session['user_id']
    # 删除所有cookie
    # session.clear()
    return redirect(url_for('home.login'))


# 上下文函数
@home.context_processor
def my_context_processor():
    # 查找cookie
    user_id=session.get('user_id')
    if user_id:
        user=UserInfo.query.filter(UserInfo.user_id==user_id).first()
        if user:
            return {'user':user}
    return {}


# 视频播放页面
@home.route('/detail/<video_id>/')
def detail(video_id):
    video_model=VideoInfo.query.filter(VideoInfo.video_id==video_id).first()
    stars = StarInfo.query.all()
    # 播放时将一条观看记录数据插入到数据库中
    if session.get('user_id'):
        watch_time = datetime.now()
        user_id = session.get('user_id')


        watch_record = WatchRelation.query.filter(WatchRelation.user_id == user_id, WatchRelation.video_id == video_id).first()
        if watch_record:
            watch_record.watch_time = watch_time
        else:
            user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
            video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()

            new_watch_record = WatchRelation(watch_time = watch_time, user_id = user_id, video_id = video_id)
            new_watch_record.watch_user = user
            new_watch_record.watch_video = video

            db.session.add(new_watch_record)
        db.session.commit()
    return render_template('home/video_detail.html',video=video_model,stars=stars)

# 添加评论函数
@home.route('/add_review/',methods=['POST'])
@login_required
def add_review():
    review_text=request.form.get('review_text')
    video_id=request.form.get('video_id')
    user_id=session['user_id']

    review=ReviewInfo(review_text=review_text,user_id=user_id,video_id=video_id,review_time=datetime.now())
    user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()

    review.review_author = user
    review.review_video = video

    db.session.add(review)
    db.session.commit()
    return redirect(url_for('home.detail',video_id = video_id))

# 点赞函数
@home.route('/like_video/')
@login_required
def like_video():
    video_id=request.args.get('video_id')
    user_id=session['user_id']

    user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
    user.user_likes.append(video)
    db.session.commit()
    return redirect(url_for('home.detail',video_id = video_id))

# 收藏函数
@home.route('/star_video/',methods=['POST'])
@login_required
def star_video():
    star_id=request.form.get('star_id')
    video_id=request.form.get('video_id')

    user_id=session['user_id']

    star_rtime = datetime.now()
    starRelation = StarRelation(star_id=star_id, star_rtime=star_rtime, video_id=video_id)
    db.session.add(starRelation)
    db.session.commit()

    return redirect(url_for('home.detail',video_id = video_id))


# 发布视频函数
@home.route('/my_video_make/',methods=['GET','POST'])
@login_required
def my_video_make():
    if request.method=='GET':
        return render_template('home/my_video_make.html')
    else:
        video_file = request.files['video_file']
        time_str = str(int(time.time()))    # 往旧的文件名加上当前时间戳避免文件重名问题
        video_url = time_str + video_file.filename
        
        if video_file:
            upload_path = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], video_url)
            video_file.save(upload_path)
        
        video_poster = request.files['video_poster']
        img_url = time_str + video_poster.filename
        if video_poster:
            upload_path = os.path.join(app.config['POSTER_UPLOAD_FOLDER'], img_url)
            video_poster.save(upload_path)
        img_info = ImgInfo(img_url = img_url)

        db.session.add(img_info)
        db.session.commit()
        #print("图片id", img_info.img_id)

        video_title = request.form.get('video_title')
        video_comment = request.form.get('video_comment')
        video_ctime = datetime.now()
        video_nlike = 0
        img_id = img_info.img_id
        user_id = session['user_id']
        video_author = UserInfo.query.filter(UserInfo.user_id==user_id).first()

        video = VideoInfo(video_title=video_title, video_comment=video_comment, video_url=video_url, video_ctime=video_ctime, video_nlike=video_nlike, img_id=img_id)
        video.video_author = video_author
        video.video_poster = img_info
        db.session.add(video)
        db.session.commit()
        print('两个文件名', video_url, ' ', img_url)
        return redirect(url_for('home.my_video_list'))

# 我的作品页面
@home.route('/my_video_list/')
@login_required
def my_video_list():
    user_id = session['user_id']
    videos = VideoInfo.query.filter(VideoInfo.user_id == user_id)
    return render_template('home/my_video_list.html',videos = videos)

# 修改视频页面
@home.route('/video_modify/', methods=['GET','POST'])
@login_required
def video_modify():
    if request.method=='GET':
        video_id = request.args.get('video_id',0)
        video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
        return render_template('home/video_modify.html',video=video)
    else:
        video_new_title = request.form.get('video_title')
        video_new_comment = request.form.get('video_comment')
        video_id = request.form.get('video_id')
        video_mtime = datetime.now()
        video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
        if video_new_title != "":
            video.video_title = video_new_title
        if video_new_comment != "":
            video.video_comment = video_new_comment
        video.video_mtime = video_mtime
        db.session.commit()
        return redirect(url_for('home.my_video_list'))

    

# 处理删除视频请求
@home.route('/video_delete/<video_id>/')
@login_required
def video_delete(video_id):
    video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('home.my_video_list'))

# 全部私聊页面
@home.route('/my_msg_list/')
@login_required
def my_msg_list():
    user_id = session['user_id']
    # 先从所有涉及到当前用户的消息取出来，再从中取出所有朋友的user_id到list中
    friend_ids = set()
    msgs = MsgInfo.query.filter(or_(MsgInfo.user_id == user_id, MsgInfo.use_user_id == user_id)).all()
    for msg in msgs:
        if(msg.user_id != user_id):
            friend_ids.add(msg.user_id)
        else:
            friend_ids.add(msg.use_user_id)
    friend_ids = list(friend_ids)
    # 获取所有朋友UserInfo
    friends = UserInfo.query.filter(UserInfo.user_id.in_(friend_ids)).all()
    return render_template('home/my_msg_list.html',friends = friends)

# 单个私聊页面
@home.route('/my_msg/<friend_id>/')
@login_required
def my_msg(friend_id):
    user_id = session['user_id']
    other_user = UserInfo.query.filter(UserInfo.user_id == friend_id).first()
    msg_list = MsgInfo.query.filter(or_(and_(MsgInfo.user_id == user_id, MsgInfo.use_user_id == friend_id), and_(MsgInfo.user_id == friend_id, MsgInfo.use_user_id == user_id))).order_by(db.desc(MsgInfo.msg_time)).all()
    return render_template('home/my_msg.html', msg_list = msg_list, other_user = other_user)

# 全部收藏夹页面
@home.route('/my_star_list/')
@login_required
def my_star_list():
    user_id = session['user_id']
    star_list = StarInfo.query.filter(StarInfo.user_id == user_id).all()
    return render_template('home/my_star_list.html',star_list = star_list)

# 单个收藏夹页面
@home.route('/my_star/<star_id>/')
@login_required
def my_star(star_id):
    star_info = StarInfo.query.filter(StarInfo.star_id == star_id).first()
    star_record_list = StarRelation.query.filter(StarRelation.star_id == star_id).order_by(db.desc(StarRelation.star_rtime)).all()
    video_list = []
    time_list = []
    for star_record in star_record_list:
        video_list.append(star_record.star_video)
        time_list.append(star_record.star_rtime)
    return render_template('home/my_star.html', video_list = video_list, star_name=star_info.star_name, time_list = time_list, list_size = len(video_list), star_id = star_id)

# 粉丝列表页面
@home.route('/my_fans/')
@login_required
def my_fans():
    user_id = session['user_id']
    fans_relation_list = FansRelation.query.filter(FansRelation.famous_user_id == user_id).all()
    fans_user_list = []
    for fans_relation in fans_relation_list:
        fans_user_list.append(fans_relation.fans_user)
    return render_template('home/my_fans.html', fans_user_list = fans_user_list)

# 关注列表页面
@home.route('/my_subscribes/')
@login_required
def my_subscribes():
    user_id = session['user_id']
    fans_relation_list = FansRelation.query.filter(FansRelation.fans_user_id == user_id).all()
    famous_user_list = []
    for fans_relation in fans_relation_list:
        famous_user_list.append(fans_relation.famous_user)
    return render_template('home/my_subscribes.html', famous_user_list = famous_user_list)

# 观看历史页面
@home.route('/my_watch_history/')
@login_required
def my_watch_history():
    user_id = session['user_id']
    watch_relation_list = WatchRelation.query.filter(WatchRelation.user_id == user_id).order_by(db.desc(WatchRelation.watch_time)).all()
    video_list = []
    for watch_relation in watch_relation_list:
        video_list.append(watch_relation.watch_video)
    
    return render_template('home/my_watch_history.html', watch_relation_list = watch_relation_list, video_list = video_list, size = len(video_list))

# 个人主页页面
@home.route('/homepage/')
@login_required
def homepage():
    return render_template('home/homepage.html')

# 创建收藏夹页面
@home.route('/my_star_make/', methods=['GET','POST'])
@login_required
def my_star_make():
    if request.method == 'GET':
        return render_template('home/my_star_make.html')
    else:
        star_name = request.form.get('star_name')
        user_id = session['user_id']
        user = UserInfo.query.filter(UserInfo.user_id == user_id).first()

        new_star = StarInfo(star_ctime = datetime.now(), user_id = user_id, star_name = star_name)
        new_star.star_user = user

        db.session.add(new_star)
        db.session.commit()
        return redirect(url_for('home.my_star_list'))

# 处理取消收藏请求
@home.route('/unstar/', methods=['GET'])
@login_required
def unstar():
    star_id = request.args.get('star_id')
    video_id = request.args.get('video_id')
    star_record = StarRelation.query.filter(StarRelation.star_id == star_id, StarRelation.video_id == video_id).first()
    db.session.delete(star_record)
    db.session.commit()
    return redirect(url_for('home.my_star', star_id = star_id))


# 他人主页页面
@home.route('/other_homepage/', methods=['GET'])
@login_required
def other_homepage():
    other_user_id = request.args.get('other_user_id')
    other_user = UserInfo.query.filter(UserInfo.user_id == other_user_id).first()
    return render_template('home/other_homepage.html', other_user = other_user)

# 他人作品列表
@home.route('/other_video_list/')
@login_required
def other_video_list():
    other_user_id = request.args.get('other_user_id')
    other_user = UserInfo.query.filter(UserInfo.user_id == other_user_id).first()
    videos = VideoInfo.query.filter(VideoInfo.user_id == other_user_id)
    return render_template('home/other_video_list.html',videos = videos, other_user = other_user)

# 处理关注请求
@home.route('/follow_user/')
@login_required
def follow_user():
    other_user_id = request.args.get('other_user_id')
    user_id = session['user_id']
    fans_relation = FansRelation.query.filter(FansRelation.famous_user_id == other_user_id, FansRelation.fans_user_id == user_id).first()
    if(fans_relation == None):
        new_fans_relation = FansRelation(famous_user_id = other_user_id, fans_user_id = user_id)
        db.session.add(new_fans_relation)
        db.session.commit()
    return redirect(url_for('home.my_subscribes'))

# 处理关注请求
@home.route('/send_msg/', methods=['POST'])
@login_required
def send_msg():
    msg_text = request.form.get('msg_text')
    receiver_id = request.form.get('receiver_id')
    msg_time = datetime.now()
    sender_id = session['user_id']

    new_msg = MsgInfo(msg_text = msg_text, msg_time = msg_time, user_id = sender_id, use_user_id = receiver_id)
    db.session.add(new_msg)
    db.session.commit()
    return redirect(url_for('home.my_msg',friend_id = receiver_id))
    

@home.route('/uploaded_file/<file_name>')
def uploaded_file(file_name):
    return send_from_directory(app.config['VIDEO_UPLOAD_FOLDER'],
                               file_name)

# 关注的up主视频页面
@home.route('/video_square/')
@login_required
def video_square():
    user_id = session['user_id']
    sql_query = "SELECT V.video_id FROM fans_relation AS FR, video_info AS V WHERE FR.fans_user_id=%d and FR.famous_user_id=V.user_id ORDER BY V.video_ctime" % user_id
    result = db.session.execute(sql_query)
    video_ids = []
    for row in result.fetchall():
        video_ids.append(row[0])
    print("id", video_ids)
    videos = VideoInfo.query.filter(VideoInfo.video_id.in_(video_ids)).all()
    return render_template('home/video_square.html',videos = videos)
        

# 下一个视频
@home.route('/next_video/')
def next_video():
    # 从数据库中随机选一个已有的video返回即可
    video_list = VideoInfo.query.all()
    if len(video_list) == 0:
        return redirect(url_for('home.index'))
    next_video = random.choice(video_list)
    if next_video:
        return redirect(url_for('home.detail', video_id = next_video.video_id))
    else:
        return redirect(url_for('home.index'))

# 删除观看记录
@home.route('/delete_watch')
@login_required
def delete_watch():
    video_id = request.args.get('video_id')
    user_id = request.args.get('user_id')
    watch = WatchRelation.query.filter(WatchRelation.user_id==user_id, WatchRelation.video_id==video_id).first()
    db.session.delete(watch)
    db.session.commit()
    return redirect(url_for('home.my_watch_history'))

# 取消一个关注
@home.route('/delete_famous_user')
@login_required
def delete_famous_user():
    famous_user_id = request.args.get('famous_user_id')
    fans_user_id = session['user_id']
    fans_record = FansRelation.query.filter(FansRelation.fans_user_id==fans_user_id, FansRelation.famous_user_id==famous_user_id).first()
    db.session.delete(fans_record)
    db.session.commit()
    return redirect(url_for('home.my_subscribes'))