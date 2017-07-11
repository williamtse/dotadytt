#coding=utf-8
from flask import Blueprint, render_template, abort, session, redirect, url_for
from db.Orms import FollowList, Article
from db.database import db_session
from flask_login import login_required


db = db_session()
follow_page = Blueprint('follow_page', __name__, template_folder='templates')

@follow_page.route('/')
def index():
    if 'user_id' in session:
        res = db.query(Article).join(FollowList, FollowList.imdbid==Article.imdbid)\
            .filter(FollowList.user_id==session['uid'])
        print res.count()
        return render_template('/follow/index.html', articles=res.all(), total=res.count())
    else:
        return redirect(url_for('user_page.login', url='/follow'))