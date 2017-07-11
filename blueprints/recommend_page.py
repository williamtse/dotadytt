#coding=utf-8
from flask import Blueprint, render_template, abort, session, redirect, url_for, jsonify, request, flash
from db.Orms import Bt, Download, Recommend
from db.database import db_session
from flask_login import login_required
from sqlalchemy import and_
import time
from models import RecommendDeleteForm



db = db_session
recommend_page = Blueprint('recommend_page', __name__, template_folder='templates')

@recommend_page.route('/delete/<btid>', methods=['GET','POST'])
def delete(btid):
    if not 'uid' in session:
        return redirect(url_for('user_page.login', url=url_for('recommend_page.delete',btid=btid)))
    res = db.query(Bt).filter(Bt.id==btid)
    if res.count()==0:
        return abort(404)
    form = RecommendDeleteForm(request.form)
    bt = res.first()
    if bt.recommended():
        flash(u'你已提交过建议')
        return redirect(url_for('bt_page.show', btid=btid))
    if request.method=='POST' and form.validate():
        recommend = Recommend(
                user_id=session['uid'],
                bt_id=btid,
                created_at=int(time.time()),
                reason = request.form['reason'],
                type='D'
            )
        db.add(recommend)
        db.commit()
        if recommend.id>0:
            bt.delete_count+=1
            db.commit()
            flash(u'删除建议已提交，等待审核')
            return redirect(url_for('bt_page.show', btid=btid))

    return render_template('recommend/delete.html', form=form, bt=bt)


@recommend_page.route('/useful/<btid>')
def useful(btid):
    if not 'uid' in session:
        return redirect(url_for('user_page.login', url=url_for('bt_page.show',btid=btid)))
    
    res = db.query(Bt).filter(Bt.id==btid)
    
    if res.count()==0:
        return abort(404)
    
    bt = res.first()
    
    if bt.recommended():
        flash(u'你已提交过建议')
        return redirect(url_for('bt_page.show', btid=btid))

    recommend = Recommend(
                user_id=session['uid'],
                bt_id=btid,
                created_at=int(time.time()),
                type='U'
            )
    db.add(recommend)
    db.commit()

    if recommend.id>0:
        bt.accept_count+=1
        db.commit()

    if recommend.id>0:
        flash(u'推荐成功')
        return redirect(url_for('bt_page.show', btid=btid))
    else:
        return abort(503)


@recommend_page.route('/report/<btid>')
def report(btid):
    if not 'uid' in session:
        return redirect(url_for('user_page.login', url=url_for('bt_page.show',btid=btid)))
    
    res = db.query(Bt).filter(Bt.id==btid)
    
    if res.count()==0:
        return abort(404)
    
    bt = res.first()
    
    if bt.recommended():
        flash(u'你已提交过建议')
        return redirect(url_for('bt_page.show', btid=btid))

    recommend = Recommend(
                user_id=session['uid'],
                bt_id=btid,
                created_at=int(time.time()),
                type='R'
            )
    db.add(recommend)
    db.commit()

    if recommend.id>0:
        flash(u'举报成功')
        return redirect(url_for('bt_page.show', btid=btid))
    else:
        return abort(503)