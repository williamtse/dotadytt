#coding=utf-8
from flask import Blueprint, render_template, abort, session, jsonify
from db.Orms import Category, MovieCategory
from db.database import db_session
import time


db = db_session()
category_page = Blueprint('category_page', __name__, template_folder='templates')


@category_page.route('/')
def index():
    pass


@category_page.route('/<aid>')
def show(aid):
    res = Category.query.filter(Category.id==aid)
    if res.count()>0:
        category = res.one()
        return render_template('category/show.html', category=category)
    else:
        abort(404)


@category_page.route('/follow/<aid>', methods=['POST'])
def follow(aid):
    if 'uid' in session:
        res = Category.query.filter(Category.id==aid)
        if res.count()>0:
            from utils.jinja_filters import followed_category
            if followed_category(aid):
                ins = MovieCategory.delete(whereclause='category_id=' + str(aid)
                                                     + ' AND user_id=' + str(session['uid']))
                res = conn.execute(ins)
                if res:
                    return jsonify({'status': 1})

            ins = MovieCategory.insert().values(category_id=aid, user_id=session['uid'],
                                              created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()))
            res = conn.execute(ins)
            if res:
                return jsonify({'status': 1})
            else:
                return jsonify({'status': -2, 'info': '500'})

        else:
            abort(404)
    else:
        return jsonify({'status':0,'info':'未登录'})