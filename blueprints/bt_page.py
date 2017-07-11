#coding=utf-8
from flask import Blueprint, render_template, abort, session, redirect, url_for, jsonify, request
from db.Orms import Bt, Download, BtVote, User, Message
from db.database import db_session
from flask_login import login_required
from sqlalchemy import and_
import time
from utils.common import now_datetime

db = db_session
bt_page = Blueprint('bt_page', __name__, template_folder='templates')


@bt_page.route('/')
def index():
    pass


@bt_page.route('/<btid>')
def show(btid):
    res = db.query(Bt).filter(Bt.id==btid)
    if res.count()==0:
        abort(404)
    bt = res.one()
    return render_template('bt/show.html', bt=bt)


@bt_page.route('/vote/<type>', methods=['POST'])
def vote(type):
    btid = request.form.get('btid')

    if not btid:
        return abort(503)

    bt = Bt.query.get(btid)
    if not bt:
        return abort(503)

    is_admin = False
    if not bt.user_id==None:
        user = User.query.get(bt.user_id)
        if not user:
            return abort(503)
    else:
        is_admin=True

    if bt.voted():
        return abort(503)

    if not 'uid' in session:
        return jsonify({'status':2})

    if type=='up':
        votetype=u'赞'
    elif type=='down':
        votetype = u'踩'.encode('utf-8')
    else:
        return abort(503)
    try:
        vote = BtVote(bt_id=btid, user_id=session['uid'], type=votetype,                           
            created_at=int(time.time()))
        db.add(vote)
        db.commit()
        if vote.id>0:
            if type=='up':
                bt.vote_count += 1
                if not is_admin:
                    user.reputation = user.reputation + 2
            else:
                bt.vote_count -= 1
                if not is_admin:
                    user.reputation = user.reputation - 2
            db.commit()
            #send message
            if not is_admin:
                content = votetype+u'了你提交的电影资源'
                msg = Message(reciver_id=user.id,
                              content=content,
                              type='btvote',
                              rel_id=btid,
                              sender_id=session['uid'],

                              created_at=now_datetime()
                              )
                db.add(msg)
                db.commit()
        else:
            return abort(503)
    except:
        db.rollback()
    return jsonify({'status': 1})
