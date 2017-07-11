#coding=utf-8
from wtforms import StringField,SubmitField,TextField
from wtforms.widgets import TextArea
from wtforms.validators import required,length,regexp,url
from models.BaseForm import BaseForm


class ArticleCreateForm(BaseForm):
    title = StringField(u'标题',[required(),length(max=60,message=u'名称太长（不超过60个字符）')])
    content = TextField(u'正文',[required()],widget=TextArea())
    pic = StringField(u'图片',[required(),url(message=u"链接格式无效")])
    brief = StringField(u'摘要',[required(),length(max=60,message=u'名称太长（不超过200个字符）')])
    rel_movies = StringField(u'关联电影',[required()])
    submit = SubmitField(u"保存")