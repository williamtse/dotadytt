#coding=utf-8
from flask import Blueprint, render_template, abort, session, redirect, url_for, jsonify, request
from db.Orms import Bt, Download, BtVote, User, Message
from db.database import db_session
from flask_login import login_required
from sqlalchemy import and_
import time
from utils.common import now_datetime

db = db_session
message_page = Blueprint('message_page', __name__, template_folder='templates')


@message_page.route('/')
def index():
    if not 'uid' in session:
        return abort(503)
    uid = session['uid']
    messages = db.query(Message).filter('')


@message_page.route('/<id>')
def show(id):
    res = db.query(Message).filter(Message.id==id)
    if res.count()==0:
        abort(404)
    bt = res.one()
    return render_template('message/show.html', bt=bt)



