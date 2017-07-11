#coding=utf-8
from flask import Blueprint, render_template, abort, session, jsonify
from db.Orms import Actor
from db.database import db_session
import time


db = db_session()
actor_page = Blueprint('actor_page', __name__, template_folder='templates')


@actor_page.route('/')
def index():
    pass


@actor_page.route('/<aid>')
def show(aid):
    res = db.query(Actor).filter(Actor.celebrity_id==aid)
    if res.count()>0:
        actor = res.one()
        return render_template('actor/show.html', actor=actor)
    else:
        abort(404)
