#coding=utf-8
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import required, length
from db.database import db_session
from jinja2 import Markup
from Base import CKTextAreaField

db = db_session()


class CelebrityView(ModelView):
    column_exclude_list = ['info']
    form_excluded_columns = ['movies','followers']
    column_formatters = dict(pic=lambda v, c, m, p: Markup('<img style="height:100px" src="'+str(m.pic)+'">'))
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    column_searchable_list = ['name']
    form_overrides = {
        'info': CKTextAreaField
    }
    form_args = {
        'name': {
            'label': u'姓名',
            'validators': [required(), length(max=100, message=u'标题不超过100个字符')]
        }
    }
