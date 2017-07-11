#coding=utf-8
from jinja2 import Markup
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import required, length
from db.database import db_session

db = db_session()


class CommentView(ModelView):
    # column_exclude_list = ['url','updated_at']
    # column_formatters = dict(
    #     title=lambda v, c, m, p: Markup('<a href="'+m.url+'">'+m.title+'</a>'))
    form_args = {
        'content': {
            'label': u'内容',
            'validators': [required(),length(max=500, message=u'标题不超过500个字符')]
        },
    }

