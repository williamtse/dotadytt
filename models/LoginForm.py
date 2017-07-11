# -*- coding: UTF-8 -*-
from models.BaseForm import BaseForm
from wtforms import Form, PasswordField, StringField, validators,HiddenField,SubmitField
from db.database import db_session
from utils.md5 import md5
from flask import session
from db.Orms import User
from sqlalchemy import and_, or_
from flask_security.utils import encrypt_password, verify_and_update_password

db = db_session


class LoginForm(BaseForm):
    username = StringField(u'用户名', [validators.Length(min=4,max=30)])
    password = PasswordField(u'密 码',[validators.Length(min=5, max=128)])
    submit = SubmitField(u'登 录')
    hidden_tag = HiddenField()
    error = ''

    def validate_login(self, form):
        if self.validate():
            user = db.query(User).filter(or_(User.name==form['username'], User.email==form['username']))
            if user.count()>0:
                usermodel = user.one()
                if not verify_and_update_password(form['password'], usermodel):
                    self.error = u'用户名或密码错误'
                    return False
                if usermodel.active==0:
                    self.error=u'用户尚未激活，登陆邮箱激活'
                    return False

                self.id = usermodel.id
                self.__setattr__('is_authenticated',True)
                session['uid'] = usermodel.id
                session['username'] = usermodel.name
                return usermodel
            else:
                self.error=u'用户'+form['username']+u'不存在'
                return False
        else:
            return False
