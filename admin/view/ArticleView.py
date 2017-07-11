#coding=utf-8
from BaseView import BaseView
from flask_admin import expose
from db.database import db_session, conn
from wtforms.validators import required
from Base import CKTextAreaField
from admin.form.ArticleEditForm import ArticleEditForm
from admin.form.ArticleCreateForm import ArticleCreateForm
from db.Orms import Article, Movie
from flask import request,redirect,url_for
from flask_admin.contrib.sqla import ModelView
from utils.common import now_datetime
from sqlalchemy.sql.expression import text

db = db_session


class ArticleView(BaseView):
    column_exclude_list = ['content','updated_at','brief','pic']
    # form_excluded_columns = ['followers']
    column_searchable_list = ['title']

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        form = ArticleCreateForm(request.form)
        if request.method=='POST' and form.validate():
            
            article = Article(
                title=request.form['title'],
                content = request.form['content'],
                pic = request.form['pic'],
                rel_movies = request.form['rel_movies'],
                brief=request.form['brief'],
                created_at=now_datetime()
                )
            db.add(article)
            db.commit()
            if article.id>0:
                rel_movies = request.form['rel_movies']
                if rel_movies:
                    arr = rel_movies.split(',')
                    if len(arr)>0:
                        for ma in arr:
                            sql  = "insert into movie_article set article_id=:aid, movie_id=:mid"
                            conn.execute(text(sql),{
                                'aid':article.id,
                                'mid':ma
                                })
                return redirect('/admin/article')
        return self.render('/admin/create_article.html', form=form)


    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        if request.method=='GET':
            id = request.args['id']
        else:
            id = request.form['id']
        article = Article.query.get(id)
        form = ArticleEditForm(request.form)
        if request.method=='POST' and form.validate():
            article.title=request.form['title']
            article.content = request.form['content']
            article.pic = request.form['pic']
            article.brief=request.form['brief']
            article.rel_movies = request.form['rel_movies']
            article.created_at=now_datetime()
            db.commit()
            rel_movies = request.form['rel_movies']
            if rel_movies:
                sql = "delete from movie_article where article_id=:aid"
                conn.execute(text(sql),{'aid':id})
                arr = rel_movies.split(',')
                if len(arr)>0:
                    for ma in arr:
                        sql  = "insert into movie_article set article_id=:aid, movie_id=:mid"
                        conn.execute(text(sql),{
                            'aid':id,
                            'mid':ma
                            })
            return redirect('/admin/article')
        return self.render('/admin/edit_article.html', form=form, article=article)


