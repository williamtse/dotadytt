#coding=utf-8
from jinja2 import Markup
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import required, length
from db.database import db_session

db = db_session()


class TrailerView(ModelView):
    column_exclude_list = ['url']
    column_formatters = dict(
        name=lambda v, c, m, p: Markup('<a href="'+m.url+'" target="_blank">'+m.name+'</a>'))
    form_args = {
        'name': {
            'label': u'标题',
            'validators': [required(),length(max=128, message=u'标题不超过128个字符')]
        },
        'url': {
            'label': u'链接',
            'validators': [required(), length(max=500, message=u'链接不超过500个字符')]
        },
    }

