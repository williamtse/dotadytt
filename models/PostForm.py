# -*- coding: UTF-8 -*-
from models.BaseForm import BaseForm
from wtforms import TextAreaField, StringField
from db.database import db_session
from wtforms.validators import required, length

db = db_session


class PostForm(BaseForm):
    title = StringField(u'标题', validators=[required(message=u'必填'), length(max=128)])
    content = TextAreaField(u'我来说两句', validators=[required(message=u'必填'),length(max=1000)])