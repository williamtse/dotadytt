#coding=utf8
from md5 import md5
from flask import session, request, url_for
from db.database import db_session
from db.Orms import FollowList, Comment
from sqlalchemy import and_
import urllib2, json
import datetime
from math import ceil
from PIL import Image, ImageFile
from conf.config import IMG_PATH
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_avatar(email,size=64):
    return 'https://secure.gravatar.com/avatar/'+md5(email)+'?s='+str(size)


def followed(imdbid):
    if 'user_id' in session:
        uid = session['user_id']
        ins = FollowList.query.filter(and_(FollowList.user_id==uid, FollowList.imdbid==imdbid))
        if ins.count()>0:
            return True
        else:
            return False
    else:
        return False


def format_time(timestamp, format='%Y-%m-%d %H:%M:%S'):
    import time
    return time.strftime(format,timestamp)


def get_location(ip):
    try:
        apiurl = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
        content = urllib2.urlopen(apiurl).read()
        data = json.loads(content)['data']
        code = json.loads(content)['code']
        if code == 0:  # success
            return data['city']
    except:
        return 'no location'


def commented(imdbid):
    try:
        db = db_session()
        if 'user_id' not in session:
            return False
        uid = session['uid']
        cmt = db.query(Comment).filter(and_(Comment.user_id==uid, Comment.imdbid==imdbid))
    finally:
        db.close()
    if cmt.count()>0:
        return True
    return False


def timeago(datetimestr):
    info = datetimestr
    print info
    now = datetime.datetime.now()

    if now.year>info.year:
        return str(now.year-info.year)+u'年前'
    elif now.month>info.month:
        return str(now.month-info.month)+u'个月前'
    elif now.day>info.day:
        return str(now.day-info.day)+u'天前'
    elif now.hour>info.hour:
        return str(now.hour-info.hour)+u'小时前'
    elif now.minute>info.minute:
        return str(now.minute-info.minute)+u'分钟前'
    else:
        return u'刚刚'


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def rating_class_num(rating_num):
    if rating_num:
    	return int(ceil(float(rating_num))*5)
    else:
	return ''

def get(name):
    return request.args.get(name)


def show_mainpic(imgname):
    if not imgname==None:
        p1 = '/mainpic/'+imgname
        p2 = '/mainpic-small/'+imgname
        if not os.path.exists(IMG_PATH+p2):
            if os.path.exists(IMG_PATH+p1):
                img = Image.open(IMG_PATH+p1)
                img = img.resize((65,100),Image.ANTIALIAS)
                img.save(IMG_PATH+p2)
        return '/img'+p2
    else:
        return '/img/movie_default_small.png'


def register_filters(app):
    env = app.jinja_env
    env.filters['get_avatar'] = get_avatar
    env.filters['followed'] = followed
    env.filters['format_time'] = format_time
    env.filters['md5'] = md5
    env.filters['str'] = str
    env.filters['get_location'] = get_location
    env.filters['commented'] = commented
    env.filters['timeago'] = timeago
    env.globals['url_for_other_page'] = url_for_other_page
    env.filters['rating_class_num'] = rating_class_num
    env.filters['get'] = get
    env.filters['show_mainpic'] = show_mainpic








