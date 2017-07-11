# -*- coding: UTF-8 -*-
from models.BaseForm import BaseForm
from wtforms import Form, PasswordField, StringField, validators,HiddenField,SubmitField, TextAreaField
from db.database import db_session
from utils.md5 import md5
from flask import session
from db.Orms import User
from sqlalchemy import and_, or_
from wtforms.validators import required, length
from flask_security.utils import encrypt_password, verify_and_update_password

db = db_session


class BtForm(BaseForm):
    title = StringField(u'标题', validators=[required(message=u'必填'), length(max=128)])
    url = TextAreaField(u'下载链接', validators=[required(message=u'必填'), length(max=1000)])
    size = StringField(u'大小', validators=[required(message=u'必填'), length(max=100)])
    format = StringField(u'格式', validators=[required(message=u'必填'), length(max=100)])
    version = StringField(u'字幕', validators=[required(message=u'必填'), length(max=100)])