#coding=utf-8
from flask import Blueprint, render_template, abort, session, redirect, url_for, jsonify
from db.Orms import Bt, Download
from db.database import db_session
from flask_login import login_required
from sqlalchemy import and_
import time



db = db_session()
download_page = Blueprint('download_page', __name__, template_folder='templates')


@download_page.route('/')
def index():
    pass


@download_page.route('/<btid>')
def download(btid):
    if 'user_id' in session:
        res = db.query(Bt).filter(Bt.id==btid)
        if res.count()==0:
            abort(404)
        bt = res.one()
        if bt:
            res = Download.query.filter(and_(Download.bt_id==bt.id, Download.user_id))
            if res.count()==0:
                download = Download(bt_id=bt.id, user_id=session['uid'], created_at=int(time.time()))
                db.add(download)
                db.commit()
            import base64
            return redirect('thunder://'+base64.b64encode('AA'+bt.url.encode('utf-8')+'ZZ'))
        else:
            abort(404)
    else:
        return redirect(url_for('user_page.login', url=url_for('bt_page.show', btid=btid)))