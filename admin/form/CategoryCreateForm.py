#coding=utf-8
from wtforms import StringField,SubmitField

from wtforms.validators import required,length
from models.BaseForm import BaseForm


class CategoryCreateForm(BaseForm):
    name = StringField(u'名称',[required(),length(max=30,message=u'名称太长（不超过30个字符）')])

    submit = SubmitField(u"保存")