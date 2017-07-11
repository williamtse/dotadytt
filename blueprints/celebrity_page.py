#coding=utf-8
from flask import Blueprint, render_template, abort, session, jsonify
from db.Orms import Celebrity, MovieCelebrity
from db.database import db_session
import time


db = db_session()
celebrity_page = Blueprint('celebrity_page', __name__, template_folder='templates')


@celebrity_page.route('/')
def index():
    pass


@celebrity_page.route('/<celebrity_id>')
def show(celebrity_id):
    res = db.query(Celebrity).filter(Celebrity.id==celebrity_id)
    if res.count()>0:
        celebrity = res.one()
        return render_template('celebrity/show.html', celebrity=celebrity)
    else:
        abort(404)
