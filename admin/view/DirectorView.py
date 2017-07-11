#coding=utf-8
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import required, length
from db.database import db_session
from jinja2 import Markup


db = db_session()


def load_pic(m):
    if m.pic:
        return Markup('<img style="height:100px" src="' + m.pic + '">')
    else:
        return Markup('<img style="height:100px" src="/static/img/celebrity-default-medium.png">')


class DirectorView(ModelView):
    form_excluded_columns = ['movies','followers']
    column_exclude_list = ['info']
    column_searchable_list = ['name']
    column_formatters = dict(pic=lambda v, c, m, p:load_pic(m) )
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_args = {
        'name': {
            'label': u'姓名',
            'validators': [required(), length(max=100, message=u'标题不超过100个字符')]
        }
    }

