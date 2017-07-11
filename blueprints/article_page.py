#coding=utf-8
from flask import Blueprint, render_template, abort, session, request, redirect, url_for
from db.Orms import Article, Comment, FeedBack
from db.database import db_session
from utils.common import now_datetime
from models import CommentForm, FeedbackForm


db = db_session()
article_page = Blueprint('article_page', __name__, template_folder='templates')

@article_page.route('/')
def index():
    pass

@article_page.route('/<aid>')
def show(aid):
    res = Article.query.filter(Article.id==aid)
    if res.count()>0:
        article = res.one()
        cmform = CommentForm(request.form)
        fbfm = FeedbackForm(request.form)
        return render_template('article/show.html', article=article, cmform=cmform, fbfm=fbfm)
    else:
        abort(404)


