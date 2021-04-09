#encoding:utf-8

from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import like_relation_table,bgm_relation_table
from models import UserInfo,ImgInfo,VideoInfo,ReviewInfo,MusicInfo,MsgInfo,StarInfo,WatchRelation,StarRelation,FansRelation
from exts import db
from decorators import login_required
from datetime import datetime
from sqlalchemy import and_,or_

app=Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 首页函数
@app.route('/')
def index():
    context={
        'videos':VideoInfo.query.all()
    }
    return render_template('index.html',**context)

# 登录函数
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
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
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'


# 注册函数
@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return render_template('regist.html')
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
                return redirect(url_for('login'))


# 注销函数
@app.route('/logout/')
def logout():
    # 删除cookie
    # session.pop('user_id')
    del session['user_id']
    # 删除所有cookie
    # session.clear()
    return redirect(url_for('login'))


# 上下文函数
@app.context_processor
def my_context_processor():
    # 查找cookie
    user_id=session.get('user_id')
    if user_id:
        user=UserInfo.query.filter(UserInfo.user_id==user_id).first()
        if user:
            return {'user':user}
    return {}


# 视频播放页面
@app.route('/detail/<video_id>/')
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
    return render_template('video_detail.html',video=video_model,stars=stars)

# 添加评论函数
@app.route('/add_review/',methods=['POST'])
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
    return redirect(url_for('detail',video_id = video_id))

# 点赞函数
@app.route('/like_video/',methods=['POST'])
@login_required
def like_video():
    video_id=request.form.get('video_id')
    user_id=session['user_id']

    user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
    user.user_likes.append(video)
    db.session.commit()
    return redirect(url_for('detail',video_id = video_id))

# 收藏函数
@app.route('/star_video/',methods=['POST'])
@login_required
def star_video():
    star_id=request.form.get('star_id')
    video_id=request.form.get('video_id')

    user_id=session['user_id']

    star_rtime = datetime.now()
    starRelation = StarRelation(star_id=star_id, star_rtime=star_rtime, video_id=video_id)
    db.session.add(starRelation)
    db.session.commit()

    return redirect(url_for('detail',video_id = video_id))


# 发布视频函数
@app.route('/my_video_make/',methods=['GET','POST'])
@login_required
def my_video_make():
    if request.method=='GET':
        return render_template('my_video_make.html')
    else:
        video_title = request.form.get('video_title')
        video_comment = request.form.get('video_comment')
        video_url = request.form.get('video_url')
        print("???url", video_url)
        video_ctime = datetime.now()
        video_nlike = 0

        user_id = session['user_id']
        video_author = UserInfo.query.filter(UserInfo.user_id==user_id).first()

        video = VideoInfo(video_title=video_title, video_comment=video_comment, video_url=video_url, video_ctime=video_ctime, video_nlike=video_nlike)
        video.video_author = video_author
        db.session.add(video)
        db.session.commit()
        return redirect(url_for('my_video_list'))

# 我的作品页面
@app.route('/my_video_list/')
@login_required
def my_video_list():
    user_id = session['user_id']
    videos = VideoInfo.query.filter(VideoInfo.user_id == user_id)
    return render_template('my_video_list.html',videos = videos)

# 修改视频页面
@app.route('/video_modify/', methods=['GET','POST'])
@login_required
def video_modify():
    if request.method=='GET':
        video_id = request.args.get('video_id',0)
        video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
        return render_template('video_modify.html',video=video)
    else:
        video_new_title = request.form.get('video_title')
        video_new_comment = request.form.get('video_comment')
        video_new_url = request.form.get('video_url')
        video_id = request.form.get('video_id')
        video_mtime = datetime.now()
        video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
        if video_new_title != "":
            video.video_title = video_new_title
        if video_new_comment != "":
            video.video_comment = video_new_comment
        if video_new_url != "":
            video.video_url = video_new_url
        video.video_mtime = video_mtime
        db.session.commit()
        return redirect(url_for('my_video_list'))

    

# 处理删除视频请求
@app.route('/video_delete/<video_id>/')
@login_required
def video_delete(video_id):
    video = VideoInfo.query.filter(VideoInfo.video_id == video_id).first()
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('my_video_list'))

# 全部私聊页面
@app.route('/my_msg_list/')
@login_required
def my_msg_list():
    user_id = session['user_id']
    # 先从所有涉及到当前用户的消息取出来，再从中取出所有朋友的user_id到list中
    friend_ids = {}
    msgs = MsgInfo.query.filter(or_(MsgInfo.user_id == user_id, MsgInfo.use_user_id == user_id)).all()
    for msg in msgs:
        if(msg.user_id != user_id):
            friend_ids.add(msg.user_id)
        else:
            friend_ids.add(msg.use_user_id)
    friend_ids = list(friend_ids)
    # 获取所有朋友UserInfo
    friends = UserInfo.query.filter(UserInfo.user_id.in_(friend_ids)).all()
    return render_template('my_msg_list.html',friends = friends)

# 单个私聊页面
@app.route('/my_msg/<friend_id>/')
@login_required
def my_msg(friend_id):
    user_id = session['user_id']
    msg_list = MsgInfo.query.filter(or_(and_(MsgInfo.user_id == user_id, MsgInfo.use_user_id == friend_id), and_(MsgInfo.user_id == friend_id, MsgInfo.use_user_id == user_id))).order_by(db.desc(MsgInfo.msg_time)).all()
    return render_template('my_msg.html', msg_list = msg_list)

# 全部收藏夹页面
@app.route('/my_star_list/')
@login_required
def my_star_list():
    user_id = session['user_id']
    star_list = StarInfo.query.filter(StarInfo.user_id == user_id).all()
    return render_template('my_star_list.html',star_list = star_list)

# 单个收藏夹页面
@app.route('/my_star/<star_id>/')
@login_required
def my_star(star_id):
    star_record_list = StarRelation.query.filter(StarRelation.star_id == star_id).order_by(db.desc(StarRelation.star_rtime)).all()
    video_list = []
    for star_record in star_record_list:
        video_list.append(star_record.star_video)
    return render_template('my_star.html', video_list = video_list, star_id = star_id)

# 粉丝列表页面
@app.route('/my_fans/')
@login_required
def my_fans():
    user_id = session['user_id']
    fans_relation_list = FansRelation.query.filter(FansRelation.famous_user_id == user_id).all()
    fans_user_list = []
    for fans_relation in fans_relation_list:
        fans_user_list.append(fans_relation.fans_user)
    return render_template('my_fans.html', fans_user_list = fans_user_list)

# 关注列表页面
@app.route('/my_subscribes/')
@login_required
def my_subscribes():
    user_id = session['user_id']
    fans_relation_list = FansRelation.query.filter(FansRelation.fans_user_id == user_id).all()
    famous_user_list = []
    for fans_relation in fans_relation_list:
        famous_user_list.append(fans_relation.famous_user)
    return render_template('my_subscribes.html', famous_user_list = famous_user_list)

# 观看历史页面
@app.route('/my_watch_history/')
@login_required
def my_watch_history():
    user_id = session['user_id']
    watch_relation_list = WatchRelation.query.filter(WatchRelation.user_id == user_id).order_by(db.desc(WatchRelation.watch_time)).all()
    video_list = []
    for watch_relation in watch_relation_list:
        video_list.append(watch_relation.watch_video)
    
    return render_template('my_watch_history.html', watch_relation_list = watch_relation_list, video_list = video_list, size = len(video_list))

# 个人主页页面
@app.route('/homepage/')
@login_required
def homepage():
    return render_template('homepage.html')

# 创建收藏夹页面
@app.route('/my_star_make/', methods=['GET','POST'])
@login_required
def my_star_make():
    if request.method == 'GET':
        return render_template('my_star_make.html')
    else:
        star_name = request.form.get('star_name')
        user_id = session['user_id']
        user = UserInfo.query.filter(UserInfo.user_id == user_id).first()

        new_star = StarInfo(star_ctime = datetime.now(), user_id = user_id, star_name = star_name)
        new_star.star_user = user

        db.session.add(new_star)
        db.session.commit()
        return redirect(url_for('my_star_list'))

# 处理取消收藏请求
@app.route('/unstar/', methods=['GET'])
@login_required
def unstar():
    star_id = request.args.get('star_id')
    video_id = request.args.get('video_id')
    star_record = StarRelation.query.filter(StarRelation.star_id == star_id, StarRelation.video_id == video_id).first()
    db.session.delete(star_record)
    db.session.commit()
    return redirect(url_for('my_star', star_id = star_id))

if __name__=='__main__':
    app.run()


