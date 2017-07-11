#coding=utf-8
from flask import Blueprint, render_template, abort
from db.Orms import Director
from db.database import db_session


db = db_session()
director_page = Blueprint('director_page', __name__, template_folder='templates')

@director_page.route('/')
def index():
    pass

@director_page.route('/<aid>')
def show(aid):
    res = db.query(Director).filter(Director.celebrity_id==aid)
    if res.count()>0:
        director = res.first()
        return render_template('director/show.html', director=director)
    else:
        abort(404)