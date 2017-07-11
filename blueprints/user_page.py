#coding=utf-8
from flask import Blueprint, render_template, flash, abort, url_for, redirect, request, current_app, jsonify, session
from utils.common import is_safe_url, now_datetime
from models import LoginForm, PostForm, User as UserM
from db.database import db_session, conn
from flask_login import login_user, logout_user, login_required
from flask_mail import Mail
from conf.ErrorCode import *
from db.Orms import User, FollowList, Actor, Movie, Article, Comment, FeedBack, Praise, Message
from utils.jinja_filters import format_time
import time
from sqlalchemy import and_
db = db_session
mail = Mail()


user_page = Blueprint('user_page', __name__, template_folder='templates')


@user_page.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    url = request.args.get('url')
    if  request.method=='POST' and form.validate_login(request.form):
        user = db.query(User).filter(User.name==request.form['username']).one()
        try:
            login_user(user)
            ip = request.remote_addr
            user.login_ip = ip
            db.commit()
        finally:
            pass
        if url is not None and is_safe_url(url):
            return redirect(url)
        else:
            return redirect('/profile/' + str(user.id))
    return render_template('user/login.html', form=form, url=url)


@user_page.route('/myspace')
@login_required
def myspace():
    return render_template('user/myspace.html')


@user_page.route('/edit-profile')
@login_required
def edit_profile():
    return render_template('user/profile-edit.html')


@user_page.route('/signup',methods=['GET','POST'])
def signup():
    from models.SignupForm import SignupForm
    from db.Orms import create_user
    form = SignupForm(request.form)
    if  request.method=='POST' and form.validate():
        form_data = request.form
        user = create_user(form_data['username'], form_data['email'], form_data['password'], False)
        if user.send_active_mail():
            flash(u'注册就快成功了，请登录邮箱激活账号')
            return redirect(url_for('index'))
    return render_template('user/signup.html', form=form)


@user_page.route('/signup_active')
def signup_active():
    username = request.args.get('user')
    token = request.args.get('token')
    if not username or not token:
	abort(403)
    user = UserM()
    if user.active(username, token):
        flash(u'邮箱验证成功')
        return redirect(url_for('user_page.login'))
    else:
        flash(user.mail_verify_error)
        return redirect(url_for('user_page.login'))


@user_page.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'status':1})


@user_page.route('/ajax-login',methods=['POST'])
def ajax_login():
    form = LoginForm(request.form)
    if form.validate_login(request.form):
        user = User.query.filter(User.name==request.form['username']).one()
        login_user(user)
        return jsonify({'status':1, 'info':u'登录成功'})
    else:
        return jsonify({'status':LOGIN_ERROR_GENERAL, 'info':u'用户名或者密码错误'})


@user_page.route('/profile/<uid>')
def profile(uid):
    tab = 'home'
    q = db.query(User).filter(User.id==uid)
    if q.count()==0:
        abort(404)
    u = q.one()
    tpl = 'profile.html'
    form = PostForm(request.form)
    articles = db.query(Article).filter(Article.user_id == uid).limit(30)
    return render_template('/user/' + tpl, user=u, post_form=form, articles=articles, tab=tab)


@user_page.route('/profile/<uid>/contribute')
def contribute(uid):
    tab = 'contribute'
    q = db.query(User).filter(User.id == uid)
    if q.count() == 0:
        abort(404)
    u = q.one()
    return render_template('/user/profile-contribute.html', user=u, tab=tab)


@user_page.route('/profile/<uid>/follow')
def follows(uid):
    tab = 'follow'
    q = db.query(User).filter(User.id == uid)
    if q.count() == 0:
        abort(404)
    u = q.one()
    follow_movies = db.query(Movie).join(FollowList, FollowList.imdbid == Movie.imdbid).filter(
        FollowList.user_id == uid).all()
    follow_actors = db.query(Actor).join(FollowList, FollowList.imdbid == Actor.imdbid).filter(
        FollowList.user_id == uid).all()
    tpl = 'profile-follow.html'
    return render_template('/user/' + tpl, user=u, follow_movies=follow_movies, follow_actors=follow_actors, tab=tab)


@user_page.route('/profile/<uid>/message')
def message(uid):
    if not 'uid' in session:
        return redirect('user_page.login')
    myuid = session['uid']
    if not int(uid)==myuid:
        return abort(503)
    db.query(Message).filter(Message.readed==0).update({
        Message.readed:1
    })
    db.commit()
    tab = 'message'
    q = db.query(User).filter(User.id == uid)
    if q.count() == 0:
        abort(404)
    u = q.one()
    tpl = 'profile-message.html'
    return render_template('/user/' + tpl, user=u, tab=tab)


@user_page.route('/user-post', methods=['POST'])
def user_post():
    try:
        if 'uid' not in session:
            abort(404)
        uid = session['uid']
        article = Article(user_id=uid, content=request.form['content'], created_at=format_time(time.gmtime()),
                          type='user',
                          title=request.form['title'],
                          imdbid='us'+str(uid))
        db.add(article)
        db.commit()
    finally:
        pass
    return redirect('/profile/'+str(uid))


@user_page.route('/comment/<mid>',methods=['POST'])
def movie_comment(mid):
    type = request.args.get('type')
    if  not type:
        type = 'movie'
    if 'username' not in session:
        return redirect(url_for('login', url=request.args.get('url')))
    try:
        
        comment = Comment(imdbid=mid,user_id=session['uid'], created_at = now_datetime(),
                          content=request.form['content'], type=type)
        db.add(comment)
        db.commit()
    finally:
        pass
    return redirect(request.args.get('url'))



@user_page.route('/feedback/<cmid>', methods=['POST'])
def comment_feedback(cmid):
    if 'user_id' not in session:
        return redirect(url_for('user_page.login', url=request.args.get('url')))
    try:
        cf = FeedBack.query.filter(and_(FeedBack.comment_id==cmid, FeedBack.user_id==session['uid']))
        if cf.count()>0:
            db.close()
            return jsonify({'status': 3})

        comment = Comment.query.filter(Comment.id == cmid).one()

        fb = FeedBack(comment_id=cmid, user_id=session['uid'], content=request.form['content'],
                      created_at=now_datetime())
        db.add(fb)
        db.commit()

        msg = Message(reciver_id=comment.user_id, type='feedback', rel_id=cmid, sender_id=session['uid'], created_at=now_datetime())
        db.add(msg)
        db.commit()
    finally:
        pass
    return redirect(request.args.get('url'))


@user_page.route('/praise', methods=['POST'])
def praise():
    if 'user_id' not in session:
        return jsonify({'status':2})
    uid = session['user_id']
    if 'comment_id' not in request.form:
        return jsonify({'status': 3})
    try:
        cmid = request.form['comment_id']
        cmt = Comment.query.filter(Comment.id==cmid).one()
        if cmt.user_id==uid:
            db.close()
            return jsonify({'status': 3})
        pr = Praise.query.filter(and_(Praise.comment_id==cmid, Praise.user_id==uid))
        if pr.count()>0:
            db.close()
            return jsonify({'status': 3})
        praise = Praise(comment_id=cmid, user_id=uid, created_at=now_datetime())
        db.add(praise)
        db.commit()
        msg = Message(reciver_id=cmt.user_id, type='praise', rel_id=cmid, sender_id=uid, created_at=now_datetime())
        db.add(msg)
        db.commit()
    finally:
        pass
    return jsonify({'status':1})


@user_page.route('/follow/<imdbid>', methods=['POST'])
def follow(imdbid):
    type = request.form['type']
    if imdbid and type in ['movie','actor','director', 'user'] and 'uid' in session:
        try:
            res = db.query(FollowList).filter_by(imdbid=imdbid, user_id=session['uid'])
            if res.count()>0:
                db.delete(res.first())
                res = db.commit()
                db.close()
                return jsonify({'status': 1})
            else:
                newfl = FollowList(imdbid=imdbid,user_id=session['uid'], created_at=format_time(time.gmtime()))
                db.add(newfl)
                res = db.commit()
                if newfl.id>0:
                    db.close()
                    return jsonify({'status':1})
                else:
                    db.close()
                    print res
                    return jsonify({'status': 0, 'info':'add follow failed'})
        finally:
            pass
    else:
        return jsonify({'status':0})


@user_page.route('/comment/<cid>')
def praise_detail(cid):
    try:
        comment = Comment.query.filter(Comment.id==cid).one()
        msgid = request.args.get('msgid')
        if msgid:
            db.query(Message).filter(Message.rel_id==cid).update({Message.readed:1})
            db.commit()
    finally:
        pass
    return render_template('/user/comment.html', comment=comment)
