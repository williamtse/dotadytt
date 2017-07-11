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


class RecommendDeleteForm(BaseForm):
    reason = StringField(u'简短理由:', validators=[length(max='100', message='字数不能超过100个字符')])