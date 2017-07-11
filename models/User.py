#coding=utf-8
from flask import session, abort
from sqlalchemy import and_
from flask_login import UserMixin
from utils.md5 import md5
from db.database import db_session
from flask_mail import Mail, Message
import time, base64
from conf.Site_config import SITE_DOMAIN


from db.Orms import(
    User as UserOrm
)

db = db_session


class User(UserMixin):
    id = None
    username = None
    is_authenticated = False
    mail_verify_error = None
    infos = None

    def getLoginUser(self):
        res = db.query(UserOrm).filter(UserOrm.id==session['uid'])
        if res.count()==0:
            return None
        else:
            self.infos = res.one()
            self.is_authenticated = True
            self.username = session['username']
            self.id = session['uid']


    def active(self,username,token):
	verify_token = base64.b64decode(token)
        res = db.query(UserOrm).filter(UserOrm.name==username)
        if res.count()==0:
	    self.mail_verify_error = username+' is not exists[verify_token:'+verify_token+']'
            return False
	user = res.one()
	if not user.verify_token== verify_token:
	    self.mail_verify_error = 'verfiy token is invalid['+verify_token+']'
	    return False
        token_end_time = res.one().token_expire
        if token_end_time < time.time():
            self.mail_verify_error = u'token已过期，请重新注册'
            res.delete()
            return False
        if res:
            res = res.update({'active':1})
            db.commit()
            return res
        else:
            self.mail_verify_error = u'无效的链接'
            return False
