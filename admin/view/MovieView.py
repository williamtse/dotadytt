#coding=utf-8
from BaseView import BaseView
from db.database import db_session
from wtforms.validators import required
from Base import CKTextAreaField
from db.Orms import Celebrity

db = db_session()


class MovieView(BaseView):
    column_exclude_list = ['pic','updated_at','info', 'trailer' ]
    form_excluded_columns = ['followers', 'articles', 'comments']
    column_searchable_list = ['name']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'info': CKTextAreaField
    }

    form_args = {
        'name': {
            'label': u'片名',
            'validators': [required()]
        },
        'trailers':{
            'label':u'预告片'
        },
        'pg': {
            'label': u'分级',
            'validators': []
        },
        'title': {
            'label': u'标题',
            'validators': [required()]
        },
        'categories': {
            'label': u'分类',
            'validators': [required()]
        },
        'actors': {
            'label': u'主演'
        },
        'areas':{
          'label':u'地区'
        },
        'year':{
            'label':u'年份'
        },
        'publish_date': {
            'label': u'上映日期',
            'validators': [required()]
        },
        'created_at': {
            'label': u'发布时间',
            'validators': [required()]
        },
        'updated_at': {
            'label': u'更新时间'
        },
        'duration':{
            'label':u'时长'
        },
        'pics': {
            'label': u'海报',
            'validators': []
        },
        'info': {
            'label': u'剧情简介',
            'validators': [required()]
        },
        'directors':{
            'label':u'导演',
            'validators': [required()]
        }
    }


