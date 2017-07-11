# -*- coding: UTF-8 -*-
from models.BaseForm import BaseForm
from wtforms import Form, TextField, StringField, TextAreaField
from db.database import db_session
from wtforms.validators import required, length
from utils.md5 import md5
from flask import session
from db.Orms import User
from sqlalchemy import and_

db = db_session


class FeedbackForm(BaseForm):
    content = TextAreaField(u'', validators=[required(message=u'必填'),length(max=1000)])