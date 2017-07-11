#coding=utf-8
from wtforms import StringField,SubmitField,TextField

from wtforms.validators import required,length,regexp,url
from models.BaseForm import BaseForm


class MovieCreateForm(BaseForm):
    name = StringField(u'电影名',[required(),length(max=60,message=u'名称太长（不超过60个字符）')])
    year = StringField(u'年份',[regexp('^[0-9]{4}$',message=u"输入四位数字年份")])
    pic = StringField(u'海报',[required(),url(message=u"链接格式无效")])
    info = TextField(u'简介',[required(),length(max=1000,message=u"简介内容太长（不超过1000个字符）")])

    submit = SubmitField(u"保存")