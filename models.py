#encoding:utf-8

from exts import db
from datetime import datetime

# # 定义用户模型
# class User(db.Model):
#     __tablename__='user'
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     telephone=db.Column(db.String(11),nullable=False)
#     username=db.Column(db.String(50),nullable=False)
#     password=db.Column(db.String(100),nullable=False)


# # 定义问题模型
# class Question(db.Model):
#     __tablename__='question'
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     title=db.Column(db.String(100),nullable=False)
#     content=db.Column(db.Text,nullable=False)
#     # now()获取的是服务器第一次运行的时间
#     # now就是每次创建一个模型的时候 都获取当前时间
#     create_time=db.Column(db.DateTime,default=datetime.now())
#     author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
#     author=db.relationship('User',backref=db.backref('questions'))


# # 定义评论模型
# class Answer(db.Model):
#     __tablename__='answer'
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     content=db.Column(db.Text,nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now())
#     question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
#     author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
#     question=db.relationship('Question',backref=db.backref('answers'))
#     author=db.relationship('User',backref=db.backref('answers'))







like_relation_table = db.Table('like_relation',
                            db.Column('video_id', db.Integer, db.ForeignKey('video_info.video_id'), primary_key=True, nullable=False),
                            db.Column('user_id', db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True, nullable=False))


bgm_relation_table = db.Table('bgm_relation',
                            db.Column('music_id', db.Integer, db.ForeignKey('music_info.music_id'), primary_key=True, nullable=False),
                            db.Column('video_id', db.Integer, db.ForeignKey('video_info.video_id'), primary_key=True, nullable=False))

# 定义用户模型
class UserInfo(db.Model):
    __tablename__='user_info'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    img_id = db.Column(db.Integer)
    user_name = db.Column(db.String(10), nullable=False)
    user_fans = db.Column(db.Integer, default=0)
    user_account = db.Column(db.String(20), nullable=False)
    user_pass = db.Column(db.String(20), nullable=False)
    user_vip = db.Column(db.Boolean, default=False)
    user_date = db.Column(db.DateTime, default=datetime.now())

    user_likes = db.relationship("VideoInfo", secondary=like_relation_table, backref="video_likers")
    #user_articles
    
# 定义图片模型
class ImgInfo(db.Model):
    __tablename__='img_info'
    img_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    img_url = db.Column(db.String(256), nullable=False)

# 定义视频模型
class VideoInfo(db.Model):
    __tablename__='video_info'
    video_id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    video_url = db.Column(db.String(256), nullable=False)
    video_title = db.Column(db.String(20), nullable=False)
    video_comment = db.Column(db.String(256))   #视频简介
    video_ctime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    video_mtime = db.Column(db.DateTime, default=datetime.now())
    video_nlike = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer,db.ForeignKey('user_info.user_id'), nullable=False)
    video_author = db.relationship("UserInfo", backref="user_articles")

    video_bgms = db.relationship("MusicInfo", secondary=bgm_relation_table, backref="music_videos")


# 定义视频评论模型
class ReviewInfo(db.Model):
    __tablename__='review_info'
    review_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    rev_review_id = db.Column(db.Integer, default=-1)
    review_text = db.Column(db.String(256), nullable=False)
    review_type = db.Column(db.Integer, default=-1)
    review_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer,db.ForeignKey('user_info.user_id'), nullable=False)
    review_author = db.relationship("UserInfo", backref="user_reviews")
    video_id = db.Column(db.Integer,db.ForeignKey('video_info.video_id'), nullable=False)
    review_video = db.relationship("VideoInfo", backref="video_reviews")

# 定义音乐模型
class MusicInfo(db.Model):
    __tablename__='music_info'
    music_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    music_url = db.Column(db.String(256), nullable=False)
    music_name = db.Column(db.String(40), nullable=False)
    music_name = db.Column(db.String(20), nullable=False)

# 定义私聊消息模型
class MsgInfo(db.Model):
    __tablename__='msg_info'
    msg_time = db.Column(db.DateTime, primary_key=True, nullable=False, default=datetime.now())
    msg_text = db.Column(db.String(256), nullable=False)

    user_id = db.Column(db.Integer,db.ForeignKey('user_info.user_id'), primary_key=True, nullable=False)
    msg_sender = db.relationship("UserInfo", backref="user_send_msgs", foreign_keys=[user_id])
    use_user_id = db.Column(db.Integer,db.ForeignKey('user_info.user_id'), primary_key=True, nullable=False)
    msg_receiver = db.relationship("UserInfo", backref="user_receive_msgs", foreign_keys=[use_user_id])

# 定义收藏夹模型
class StarInfo(db.Model):
    __tablename__='star_info'
    star_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    star_ctime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user_info.user_id'), nullable=False)
    star_name = db.Column(db.String(30), nullable=False)
    star_user = db.relationship("UserInfo", backref="user_stars")

# 定义观看记录模型
class WatchRelation(db.Model):
    __tablename__='watch_relation'
    watch_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user_info.user_id'), nullable=False, primary_key=True)
    video_id = db.Column(db.Integer,db.ForeignKey('video_info.video_id'), nullable=False, primary_key=True)

    watch_user = db.relationship("UserInfo", backref="user_watchs")
    watch_video = db.relationship("VideoInfo", backref="video_watchers")

# 定义收藏记录模型
class StarRelation(db.Model):
    __tablename__='star_relation'
    star_rtime = db.Column('star_rtime', db.DateTime, nullable=False, default=datetime.now())
    star_id = db.Column(db.Integer,db.ForeignKey('star_info.star_id'), nullable=False, primary_key=True)
    video_id = db.Column(db.Integer,db.ForeignKey('video_info.video_id'), nullable=False, primary_key=True)

    star_book = db.relationship("StarInfo", backref="star_records")
    star_video = db.relationship("VideoInfo", backref="video_starers")

# 定义关注模型
class FansRelation(db.Model):
    __tablename__='fans_relation'
    famous_user_id = db.Column(db.Integer,db.ForeignKey('user_info.user_id'), nullable=False, primary_key=True)
    fans_user_id = db.Column(db.Integer,db.ForeignKey('user_info.user_id'), nullable=False, primary_key=True)

    famous_user = db.relationship("UserInfo", backref="user_fans_records", foreign_keys=[famous_user_id])
    fans_user = db.relationship("UserInfo", backref="user_subcribes_records", foreign_keys=[fans_user_id])
