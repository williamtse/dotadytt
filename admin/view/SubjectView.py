#coding=utf-8
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import required, length
from db.database import db_session
from jinja2 import Markup
from Base import CKTextAreaField

db = db_session()


class SubjectView(ModelView):
    form_excluded_columns = ['movies']
    form_args = {
        'name': {
            'label': u'主题',
            'validators': [required(), length(max=100, message=u'标题不超过100个字符')]
        }
    }