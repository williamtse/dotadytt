#coding=utf-8
from jinja2 import Markup
from BaseView import BaseView
from wtforms.validators import required, length
from db.database import db_session

db = db_session()


class BtView(BaseView):
    column_searchable_list = ['title']
    column_exclude_list = ['url','updated_at']
    column_formatters = dict(
        title=lambda v, c, m, p: Markup('<a href="'+m.url+'">'+m.title+'</a>'))
    form_args = {
        'title': {
            'label': u'标题',
            'validators': [required(),length(max=128, message=u'标题不超过128个字符')]
        },
        'url': {
            'label': u'下载链接',
            'validators': [required(), length(max=500, message=u'链接不超过500个字符')]
        },
        'size': {
            'label': u'资源大小',
            'validators': [required(), length(max=30, message=u'大小不超过30个字符')]
        },
        'version':{
            'label':u'版本信息',
            'validators': [required(), length(max=20, message=u'版本信息不超过20个字符')]
        },
        'format':{
            'label':u'文件格式',
            'validators': [required(), length(max=10, message=u'格式不超过10个字符')]
        },
        'created_at':{
            'label':u'发布时间'
        },
        'updated_at':{
            'label': u'更新时间'
        }
    }


