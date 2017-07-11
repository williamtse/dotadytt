#coding=utf-8
from jinja2 import Markup
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import required, length
from db.database import db_session

db = db_session()


class YearView(ModelView):
    form_excluded_columns = ['movies']
    form_args = {
        'year':{
            'label':u'上映年份区间',
            'validators':[required()]
        }
    }