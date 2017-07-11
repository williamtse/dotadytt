# -*- coding: UTF-8 -*-

from flask import (
    Flask, session, url_for, abort, redirect, request
)
from sqlalchemy import and_, or_
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from db.Orms import Movie,Category, Carousel, Article, User, Actor, Director
from db.database import db_session
from utils.common import init_mail
from utils.jinja_filters import register_filters
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
#blueprints
from blueprints import movie_page, user_page, article_page, celebrity_page, category_page, follow_page,download_page, bt_page,recommend_page
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from admin.view import (
    MovieView,BtView, ArticleView,  PicView, CommentView, SubjectView, CelebrityView,
    YearView, AreaView, ActorView, DirectorView
)
from db.Orms import (
    Movie,Category, Bt, Article, Pic, Carousel, Comment, Year, Area, Subject, Celebrity
)
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from db.Orms import Role
from flask_admin import helpers as admin_helpers
from admin.view.BaseView import BaseView

from flask import render_template
import time
from utils.common import Pagination, now_datetime

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_pyfile('conf/config.py')



init_mail(app)
Bootstrap(app)
register_filters(app)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    db = db_session
    # movie_categories = Category.query.all()
    # carousels = db.query(Carousel).filter(Carousel.position=='home-top').all()
    articles = Article.query.order_by(Article.created_at.desc()).limit(15)
    t = time.localtime()
    year = t.tm_year
    newest = db.query(Movie).filter(and_(Movie.publish_date<now_datetime(),Movie.year==2017)).order_by(Movie.read_count.desc()).limit(20).all()

    return render_template('index.html',newest=newest, articles=articles)



app.register_blueprint(movie_page, url_prefix='/movie')
app.register_blueprint(user_page)
app.register_blueprint(article_page, url_prefix='/article')
app.register_blueprint(celebrity_page, url_prefix='/celebrity')
app.register_blueprint(category_page, url_prefix='/category')
app.register_blueprint(follow_page, url_prefix='/follow')
app.register_blueprint(bt_page, url_prefix='/bt')
app.register_blueprint(download_page, url_prefix='/download')
app.register_blueprint(recommend_page, url_prefix='/recommend')



init_mail(app)
db = SQLAlchemy(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


admin = Admin(app,name=u'后台管理', template_mode='bootstrap3')


admin.add_view(BaseView(Role, db.session))
admin.add_view(BaseView(User, db.session))
admin.add_view(BaseView(Category, db.session ,name=u'电影分类'))
admin.add_view(MovieView(Movie, db.session ,name=u'电影'))
admin.add_view(ArticleView(Article, db.session, name=u'资讯'))
admin.add_view(BtView(Bt, db.session ,name=u'BT'))
admin.add_view(PicView(Pic, db.session, name=u'海报'))
admin.add_view(BaseView(Carousel, db.session, name=u'轮播'))
admin.add_view(CommentView(Comment, db.session, name=u'评论'))
admin.add_view(AreaView(Area, db.session, name=u'地区'))
admin.add_view(YearView(Year, db.session, name=u'年份'))
admin.add_view(SubjectView(Subject, db.session, name=u'题材'))
# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


if __name__ == '__main__':
        app.debug = True
        app.run(host='0.0.0.0', port=9000)
