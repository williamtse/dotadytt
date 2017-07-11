#coding=utf8
from flask import session,request
import urlparse
from conf.Site_config import *
from db.database import db_session
from math import ceil
import urllib
from conf.config import PATH_SEP

db = db_session


def isLogin():
    return 'user_id' in session


def session(key):
    return session[key]


def is_safe_url(target):
    ref_url = urlparse.urlparse(request.host_url)
    test_url = urlparse.urlparse(urlparse.urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def init_mail(app):
    from flask_mail import Mail
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USER_TLS
    app.config['MAIL_USE_SSL'] = MAIL_USER_SSL
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_DEBUG'] = MAIL_DEBUG
    mail = Mail()
    mail.init_app(app)
    return mail


def now_datetime(format='%Y-%m-%d %H:%M:%S'):
    import time
    return time.strftime(format, time.localtime())


def send_message(user_id, content):
    from db.Orms import Message
    msg = Message(user_id=user_id, content=content, created_at=now_datetime())
    db.add(msg)
    db.commit()

def send_async_email(app, mail, msg):
    with app.app_context():
        mail.send(msg)

from math import ceil


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

def movie_imdbid_exists(imdbid):
    url = "http://www.imdb.com/title/"+imdbid+"/"
    status = urllib.urlopen(url).code
    if status==200:
        return True
    return False


#根据文件名创建文件
def createFileWithFileName(localPathParam,fileName):
    totalPath=localPathParam+PATH_SEP+fileName
    if not os.path.exists(totalPath):
        file=open(totalPath,'a+')
        file.close()
        return totalPath


#根据图片的地址，下载图片并保存在本地
def getAndSaveImg(imgUrl, localPath):
    if( len(imgUrl)!= 0 ):
        filearr = imgUrl.split('/')
        fileName= filearr[len(filearr)-1]
        urllib.urlretrieve(imgUrl,createFileWithFileName(localPath,fileName))
        return fileName