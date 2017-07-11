#coding=utf-8
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import required, length
from db.database import db_session

db = db_session()


class PicView(ModelView):
    column_exclude_list = ['url']
    form_args = {
        'name': {
            'label': u'图片唯一名称',
            'validators': [required(), length(max=100, message=u'标题不超过100个字符')]
        }
    }