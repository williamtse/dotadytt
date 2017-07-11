#coding=utf-8
from sqlalchemy import (
    Column, String, Integer, Text, Table, ForeignKey,DateTime,Date,
    Boolean, and_, Enum, DECIMAL
)
from sqlalchemy.orm import relationship, backref
from flask import session
from flask_mail import Mail, Message as MailMessage
from flask_security import RoleMixin, UserMixin
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.sql import text
import time
from utils.md5 import md5
import base64
from utils.common import send_async_email, now_datetime
from threading import Thread
from db.database import db_session, conn


app = Flask(__name__)
app.config.from_pyfile('../conf/config.py')

db_ = SQLAlchemy(app)

db = db_session
Base = db_.Model
Base.query = db.query_property()

mail = Mail()
mail.init_app(app)




# class MovieCategory(Base):
#     __tablename__ = 'movie_category'
#     id = Column(Integer, primary_key=True)
#     category_id = Column(Integer, ForeignKey('category.id',ondelete='cascade'))
#     movie_id = Column(Integer, ForeignKey('movie.id', ondelete='cascade'))
#
#     movie = relationship('Movie', back_populates='categories', uselist=False)
#     category = relationship('Category', back_populates='movies',uselist=False)
#
#     def __str__(self):
#         return self.category.name
# Define models
roles_users = Table(
    'roles_users',
    Base.metadata,
    Column('user_id', Integer(), ForeignKey('users.id')),
    Column('role_id', Integer(), ForeignKey('role.id'))
)


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __str__(self):
        return self.name


MovieCategory = Table('movie_category', Base.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('movie_id', Integer, ForeignKey('movie.id', ondelete='cascade')),
                      Column('category_id', Integer, ForeignKey('category.id', ondelete='cascade'))
                      )


# class MovieActor(Base):
#     __tablename__='movie_actor'
#     id = Column(Integer, primary_key=True)
#     movie_id = Column(Integer, ForeignKey('movie.id', ondelete='cascade'))
#     actor_id = Column(Integer, ForeignKey('actor.id', ondelete='cascade'))
#     movie = relationship('Movie', back_populates='actors', uselist=False)
#     actor = relationship('Actor', back_populates='movies', uselist=False)
#
#     def __str__(self):
#         return self.actor.name
MovieActor = Table(
    'movie_actor',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='cascade')),
    Column('celebrity_id', Integer, ForeignKey('actor.id', ondelete='cascade'))
)


# class MovieDirector(Base):
#     __tablename__ = 'movie_director'
#     id = Column(Integer, primary_key=True)
#     movie_id = Column(Integer, ForeignKey('movie.id', ondelete='cascade'))
#     director_id = Column(Integer, ForeignKey('director.id', ondelete='cascade'))
#     movie = relationship('Movie', back_populates='directors', uselist=False)
#     director = relationship('Director', back_populates='movies', uselist=False)
#
#     def __str__(self):
#         return self.director.name
MovieDirector = Table(
    'movie_director',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='cascade')),
    Column('celebrity_id', Integer, ForeignKey('director.id', ondelete='cascade'))
)


MovieCelebrity = Table(
    'movie_celebrity',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='cascade')),
    Column('celebrity_id', Integer, ForeignKey('celebrity.id', ondelete='cascade')),
    Column('celebrity_type', Enum('actor','director'))
    )

# class MovieArea(Base):
#     __tablename__ = 'movie_area'
#     id = Column(Integer(), primary_key=True)
#     movie_id = Column(Integer(), ForeignKey('movie.id', ondelete='cascade'))
#     area_id = Column(Integer(), ForeignKey('area.id', ondelete='cascade'))
#
#     movie = relationship("Movie", back_populates='areas', uselist=False)
#     area = relationship("Area", back_populates='movies', uselist=False)
#
#     def __str__(self):
#         return self.area.name
MovieArticle = Table(
    'movie_article',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='cascade')),
    Column('article_id', Integer, ForeignKey('article.id', ondelete='cascade'))
    )


MovieArea = Table(
    'movie_area',
    Base.metadata,
    Column('id', Integer(), primary_key=True),
    Column('movie_id', Integer(), ForeignKey('movie.id', ondelete='cascade')),
    Column('area_id', Integer, ForeignKey('area.id', ondelete='cascade'))
)

MovieSubject = Table(
    'movie_subject',
    Base.metadata,
    Column('id', Integer(), primary_key=True),
    Column('movie_id', Integer(), ForeignKey('movie.id', ondelete='cascade')),
    Column('subject_id', Integer, ForeignKey('subject.id', ondelete='cascade'))
)


MovieFavorite = Table(
    'movie_favorite',
    Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('user_id',Integer, ForeignKey('users.id', ondelete='cascade')),
    Column('movie_id',Integer, ForeignKey('movie.id', ondelete='cascade')),
    Column('created_at',DateTime)
    )


class MovieRead(Base):
    __tablename__='movie_read',
    id=Column(Integer, primary_key=True)
    ip=Column(String(16))
    movie_id=Column(Integer, ForeignKey('movie.id', ondelete='cascade'))
    created_at=Column(DateTime)

    movie = relationship('Movie', back_populates='reads')


class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer(), primary_key=True)
    name = Column(String(20))

    movies = relationship('Movie',secondary=MovieArea, lazy='dynamic')

    def __str__(self):
        return self.name


class Year(Base):
    __tablename__ = 'year'
    id = Column(Integer(), primary_key=True)
    year = Column(String(50))


    def __str__(self):
        return self.year


class FollowList(Base):
    __tablename__ = 'follow_list'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    imdbid = Column(String(30))
    created_at = Column(DateTime)


class Article(Base):
    __tablename__='article'
    id = Column(Integer(), primary_key=True)
    type = Column(String(10), nullable=False, default='movie')
    pic = Column(String(500))
    title = Column(String(128))
    brief = Column(String(500))
    content = Column(Text())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    rel_movies = Column(String(1000))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))

    user = relationship('User', back_populates='articles', uselist=False)
    movies = relationship('Movie', secondary=MovieArticle)

    def __str__(self):
        return self.title

    def comments(self):
        return db.query(Comment).filter(and_(Comment.imdbid==self.id, Comment.type=='article')).all()


class Bt(Base):
    __tablename__ = 'bt'
    id = Column(Integer(), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='cascade'))
    title = Column( String(128))
    url  = Column(String(500))
    size = Column(String(30))
    version = Column(String(20))
    format = Column(String(10))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    status = Column(Enum(u'正常', u'建议删除', u'采纳'))
    vote_count = Column(Integer, nullable=False, default=0)
    accept_count = Column(Integer, nullable=False, default=0)
    delete_count = Column(Integer, nullable=False, default=0)


    movie = relationship('Movie', back_populates='bts', uselist=False)
    downloads = relationship('Download', back_populates='bt')
    user = relationship('User', back_populates='bts', uselist=False)
    recommends = relationship('Recommend', back_populates='bt', lazy='dynamic')
    votes = relationship('BtVote', back_populates='bt', lazy='dynamic')

    def __str__(self):
        return self.title

    def recommended(self):
        if 'uid' in session:
            uid = session['uid']
            r = Recommend.query.filter(and_(Recommend.bt_id==self.id, Recommend.user_id==uid))
            if r.count()>0:
                return True
        return False

    def voted(self):
        if 'uid' in session:
            uid = session['uid']
            r = db.query(BtVote).filter(and_(BtVote.bt_id==self.id, BtVote.user_id==uid))
            if r.count()>0:
                return True
        return False


class BtVote(Base):
    __tablename__ = 'bt_vote'
    id = Column(Integer, primary_key=True)
    bt_id = Column(Integer, ForeignKey('bt.id', ondelete='cascade'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    type = Column(Enum(u'赞',u'踩'))
    created_at = Column(Integer)

    bt = relationship('Bt', back_populates='votes', uselist=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer(), primary_key=True)
    name = Column(String(20))

    movies = relationship("Movie", secondary=MovieCategory, lazy='dynamic')

    def __str__(self):
        return self.name


#影人
class Celebrity(Base):
    __tablename__ = 'celebrity'
    id = Column(Integer(), primary_key=True)
    celebrity_id = Column(Integer)
    name = Column(String(100))
    pic = Column(String(500))
    info = Column(Text)
    birthday=Column(String(20))
    born = Column(String(300))
    imdbid = Column(String(30))
    jobs = Column(String(100))
    sex = Column(Enum(u'男',u'女'))
    horoscope = Column(Enum(u'双子座', u'狮子座', u'天秤座', u'金牛座', u'白羊座', u'天蝎座',
                            u'水瓶座', u'摩羯座', u'巨蟹座', u'处女座', u'双鱼座', u'射手座'))
    type = Column(Enum('director', 'actor', 'scriptwriter'))
    has_profile = Column(Boolean, nullable=False, default=1)

    movies = relationship("Movie", secondary=MovieCelebrity)

    def __str__(self):
        return self.name


class Director(Base):
    __tablename__ = 'director'

    id = Column(Integer(), primary_key=True)
    celebrity_id = Column(Integer)
    name = Column(String(100))
    pic = Column(String(500))
    info = Column(Text)
    birthday = Column(String(20))
    born = Column(String(300))
    imdbid = Column(String(30))
    jobs = Column(String(100))
    sex = Column(Enum(u'男', u'女'))
    horoscope = Column(Enum(u'双子座', u'狮子座', u'天秤座', u'金牛座', u'白羊座', u'天蝎座',
                            u'水瓶座', u'摩羯座', u'巨蟹座', u'处女座', u'双鱼座', u'射手座'))
    has_profile = Column(Boolean, nullable=False, default=1)

    movies = relationship("Movie", secondary=MovieDirector)

    def __str__(self):
        return self.name


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer(), primary_key=True)
    title = Column(String(128))
    name = Column(String(20))
    publish_date = Column(Date())
    info = Column(Text())
    pg = Column(Integer())
    duration = Column(Integer())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    year_id = Column(Integer(), ForeignKey('year.id'))
    imdbid = Column(String(30))
    pic = Column(String(500))
    year = Column(Integer)
    rating_num = Column(DECIMAL(2,1))
    read_count=Column(Integer, nullable=False, default=0)
    favorite_count = Column(Integer, nullable=False,default=0)
    bt_count = Column(Integer, nullable=False, default=0)
    first_show = Column(Date)
    season = Column(Integer)
    episode = Column(Integer)
    film_length = Column(String(30))

    areas = relationship('Area', secondary=MovieArea)
    categories = relationship("Category", secondary=MovieCategory, lazy='subquery')
    actors = relationship('Actor', secondary=MovieActor)
    bts = relationship('Bt', back_populates='movie', lazy='dynamic')
    directors = relationship('Director', secondary=MovieDirector)
    # trailers = relationship('Trailer', back_populates='movie')
    pics = relationship('Pic', back_populates='movie')
    subjects = relationship('Subject', secondary=MovieSubject, lazy='dynamic')
    #directors = relationship("Celebrity",primaryjoin=Celebrity.type=="director", secondary=MovieCelebrity)
    favorites = relationship('User', secondary=MovieFavorite, lazy='dynamic')
    reads = relationship('MovieRead', back_populates='movie', lazy='dynamic')
    articles = relationship('Article', secondary=MovieArticle, lazy='dynamic')

    def __str__(self):
        return self.name

    def comments(self):
        return db.query(Comment).filter(Comment.imdbid==self.id).all()

    def douban_comments(self):
        return db.query(DoubanComment).filter(DoubanComment.movie_id==self.id).all()

    def followers(self):
        return db.query(User).join(FollowList,FollowList.user_id==User.id).filter(FollowList.imdbid==self.imdbid)

    def favorited(self):
        if not 'uid' in session:
            return False
        uid = session['uid']
        sql = "select * from movie_favorite where movie_id=:mid and user_id=:uid"
        res = conn.execute(text(sql),{
            'mid':self.id,
            'uid':uid
            })
        if res.fetchone():
            return True
        return False


class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer(), primary_key=True)
    celebrity_id = Column(Integer)
    name = Column(String(100))
    pic = Column(String(500))
    info = Column(Text)
    birthday = Column(String(20))
    born = Column(String(300))
    imdbid = Column(String(30))
    jobs = Column(String(100))
    sex = Column(Enum(u'男', u'女'))
    horoscope = Column(Enum(u'双子座', u'狮子座', u'天秤座', u'金牛座', u'白羊座', u'天蝎座',
                            u'水瓶座', u'摩羯座', u'巨蟹座', u'处女座', u'双鱼座', u'射手座'))
    has_profile = Column(Boolean, nullable=False, default=1)

    movies = relationship("Movie", secondary=MovieActor)

    def __str__(self):
        return self.name


#预告片
# class Trailer(Base):
#     __tablename__ = 'trailer'
#     movie_id = Column(Integer, ForeignKey('movie.id', ondelete='cascade'))
#     id = Column(Integer(), primary_key=True)
#     name = Column(String(128))
#     url = Column(String(500))
#     movie = relationship('Movie', back_populates='trailers', uselist=False)
#
#     def __str__(self):
#         return self.name


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    email = Column(String(128), unique=True)
    name = Column(String(12), unique=True)
    password = Column(String(500), nullable=False)
    verify_token = Column(String(200))
    token_expire = Column(Integer())
    active = Column(Boolean())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    login_ip = Column(String(15))
    status = Column(Enum(u'正常', u'被举报'))
    reputation = Column(Integer, nullable=False, default=0)

    comments = relationship('Comment', back_populates='user')
    downloads = relationship('Download', back_populates='user')
    articles = relationship('Article', back_populates='user')
    feedbacks = relationship('FeedBack',back_populates='user')
    praises = relationship('Praise', back_populates='user')
    send_messages = relationship('Message', back_populates='sender')
    roles = relationship('Role', secondary=roles_users,
                            backref=backref('users', lazy='dynamic'))
    favorite_movies = relationship(Movie, secondary=MovieFavorite)

    bts = relationship('Bt', back_populates='user')

    def is_active(self):
        return self.actived

    def __str__(self):
        return self.name

    def id_attribute(self):
        return self.id

    def messages(self):
        res = Message.query.filter(and_(Message.reciver_id==self.id, Message.readed==0))
        return res

    def all_messages(self):
        res = Message.query.filter(Message.reciver_id == self.id)
        return res

    def send_active_mail(self):
        with app.app_context():
            print 'send active mail to '+self.email
            email = self.email
            username = self.name
            active_token = md5(email + str(self.token_expire) + app.config['SECRET_KEY'])
            msg = MailMessage(u"DOTA电影天堂-欢迎-请验证邮箱地址",
                          sender=u"DOTA电影天堂用户注册<312586329@qq.com>",
                          recipients=[email])
            token = base64.b64encode(active_token)
            domain = app.config['SITE_DOMAIN']
            url = domain+'/signup_active?user='+username+'&token='+token
            msg.html = '<h1 style="text-align:center"><a href="'+domain\
            +'" target="_blank"><img src="'+domain+'/static/img/logo.png"></h1><p><a href="'+url+'">'+url+'</a></p>'

            thread = Thread(target=send_async_email, args=[app, mail, msg])
            thread.start()
	    return True


class Pic(Base):
    __tablename__ = 'pic'
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'))
    id = Column(Integer(), primary_key=True)
    url = Column(String(500))
    name = Column(String(100), unique=True)

    movie = relationship('Movie', back_populates='pics', uselist=False)

    def __str__(self):
        return self.name


CarouselPic = Table('carouse_pic', Base.metadata,
                    Column('id',Integer(), primary_key=True),
                    Column('pic_id',Integer(), ForeignKey('pic.id', ondelete='cascade')),
                    Column('carousel_id',Integer(), ForeignKey('carousel.id', ondelete='cascade'))
                    )


#轮播
class Carousel(Base):
    __tablename__ = 'carousel'
    id = Column(Integer(), primary_key=True)
    position = Column(String(30))
    sort_num = Column(Integer(), nullable=False, default=0)

    pics = relationship('Pic', secondary=CarouselPic)

    def __str__(self):
        return self.position+str(self.id)


class Praise(Base):
    __tablename__ = 'praise'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    comment_id = Column(Integer, ForeignKey('comment.id', ondelete='cascade'))
    created_at = Column(DateTime)

    comment = relationship('Comment', back_populates='praises', uselist=False)
    user = relationship('User', back_populates='praises', uselist=False)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer(), primary_key=True)
    imdbid = Column(String(30))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)
    type = Column(String(30), nullable=False, default='movie')

    user = relationship('User',  back_populates="comments", uselist=False)
    feedbacks = relationship('FeedBack', back_populates='comment')
    praises = relationship('Praise', back_populates='comment')

    def feedback_able(self):
        if 'user_id' not in session:
            return True
        uid = session['uid']

        fb = db.query(FeedBack).filter(and_(FeedBack.user_id==uid, FeedBack.comment_id==self.id))
        if fb.count()>0:
            return False
        return True

    def get_movie(self):
        return db.query(Movie).filter(Movie.id==self.imdbid).one()

    def get_article(self):
        return db.query(Article).filter(Article.id==self.imdbid).one()


class Download(Base):
    __tablename__ = 'download'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'),nullable=False)
    bt_id = Column(Integer, ForeignKey('bt.id', ondelete='cascade'),nullable=False )
    created_at = Column(Integer)

    user = relationship('User', back_populates='downloads', uselist=False)
    bt = relationship('Bt', back_populates='downloads', uselist=False)


class FeedBack(Base):
    __tablename__='comment_feedback'
    id = Column(Integer,primary_key=True)
    comment_id = Column(Integer,ForeignKey('comment.id', ondelete='cascade'),nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'), nullable=False)

    comment = relationship('Comment',back_populates="feedbacks", uselist=False)
    user = relationship('User', back_populates='feedbacks', uselist=False)


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    reciver_id = Column(Integer)
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    content = Column(String(128))
    type = Column(String(20), nullable=False, default='comment')
    rel_id = Column(String(30), nullable=False)
    created_at = Column(DateTime)
    readed = Column(Boolean, nullable=False, default=0)

    sender = relationship('User', back_populates='send_messages', uselist=False)


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))

    movies = relationship('Movie', secondary=MovieSubject, lazy='subquery')

    def __str__(self):
        return self.name


class DoubanComment(Base):
    __tablename__ = 'douban_comment'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='cascade'))
    content = Column(Text)


class Recommend(Base):
    __tablename__ = 'recommend'
    id = Column(Integer, primary_key=True)
    bt_id = Column(Integer, ForeignKey('bt.id', ondelete='cascade'))
    reason = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    type = Column(String(2))
    created_at = Column(Integer)

    bt = relationship('Bt', back_populates='recommends', uselist=False)


class Favorite(Base):
    __tablename__='favorite'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    name = Column(String(100), nullable=False, default=u'未命名收藏夹')
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Collection(Base):
    __tablename__ = 'collection'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    favorite_id = Column(Integer, ForeignKey('favorite.id', ondelete='cascade'))
    rel_id = Column(Integer, nullable=False)
    type = Column(Enum('movie','article','bt'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


# def after_insert_bt_listener(mapper, connection, target):
#     print target.title
#     mid = target.movie_id
#     movie = db.query(Movie).filter(Movie.id==mid).first()
#     followers = movie.followers().all()
#     recipients = []
#     for flw in followers:
#         recipients.append(flw.email)

#     if len(recipients):
    
#         msg = MailMessage(target.movie.title+u"下载链接",
#                               sender=u"DOTA电影天堂用户注册<312586329@qq.com>",
#                               recipients=recipients)
#         url = app.config['SITE_DOMAIN']+'/movie/'+str(target.movie_id)+'#bts'
#         msg.html = '<p><a href="'+url+'">'+target.title+'</a></p>'
#         res = mail.send(msg)


# event.listen(Bt, 'after_insert', after_insert_bt_listener)


def create_role(name):
    db_.create_all()
    with app.app_context():
        user_role = Role(name=name)
        db.add(user_role)
        db.commit()
    


def create_user(name, email, password, superuser=True):
    user_role = Role.query.filter(Role.name=='user').one()
    roles = []
    roles.append(user_role)
    verify_token = None
    token_expire = None
    active = 1
    if superuser:
        super_user_role = Role.query.filter(Role.name=='superuser').one()
        roles.append(super_user_role)
    else:
        active = 0
        token_expire = int(time.time())+3600*24
        verify_token = md5(email + str(token_expire) + app.config['SECRET_KEY'])

    user = User(
        name=name,
        email=email,
        password=encrypt_password(password),
        roles=roles,
        verify_token=verify_token,
        token_expire=token_expire,
        active = active,
        status = u'正常',
        created_at = now_datetime()
    )
    db.add(user)
    db.commit()
    return user


