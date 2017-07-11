#coding=utf-8
from flask import Blueprint, render_template, abort, request, url_for, redirect, session, jsonify
from db.Orms import Movie, Year, Area, Category, MovieCategory, Celebrity, MovieCelebrity, Bt, MovieFavorite, MovieRead, db_session
from db.database import  conn
from models import LoginForm, CommentForm, FeedbackForm, BtForm
from datetime import datetime, timedelta
from sqlalchemy import and_, or_
from sqlalchemy.sql import text
from utils.common import Pagination, now_datetime

db = db_session

movie_page = Blueprint('movie_page', __name__, template_folder='templates')


@movie_page.route('/')
def index():
    now = datetime.now()
    week_today = now.weekday()
    datetime_now_min_1 = now-timedelta(days=week_today+1)
    week_last_day_add_1 = now+timedelta(days=7-week_today)
    week_last_day = now + timedelta(days=7-week_today-1)
    movies = db.query(Movie).filter(and_(Movie.publish_date>datetime_now_min_1,
                                         Movie.publish_date<week_last_day_add_1))\
        .order_by('created_at desc').all()

    coming_soon = db.query(Movie).filter(and_(Movie.publish_date>week_last_day))\
        .order_by('created_at desc').limit(30)
    tab = u'院线上映'
    login_form = LoginForm(request.form)

    return render_template('movie/index.html',movies=movies, tab=tab,
                           form=login_form,
                           coming_soon=coming_soon)


@movie_page.route('/<mid>')
def show(mid):
    res =  db.query(Movie).filter(Movie.id==mid)
    if res.count()==0:
        abort(404)
    else:
        movie = res.one()
        ip = request.remote_addr
        res = db.query(MovieRead).filter(MovieRead.ip==ip, MovieRead.movie_id==mid)
        if res.count()==0:
            mr = MovieRead(
                    ip=ip,
                    movie_id=mid,
                    created_at=now_datetime()
                )
            db.add(mr)
            db.commit()
            if mr.id>0:
                movie.read_count+=1
                db.commit()

        form = LoginForm(request.form)
        cmform = CommentForm(request.form)
        fbfm = FeedbackForm(request.form)
        followers = movie.followers().all()
        sql = "select c.*,mc.celebrity_type from movie_celebrity mc LEFT JOIN celebrity c on c.id=mc.celebrity_id WHERE mc.movie_id=:movie_id"
        celebrities = conn.execute(text(sql), {'movie_id':mid})
        actors = []
        directors = []
        for cel in celebrities:
            if cel.celebrity_type==u'演员':
                actors.append(cel)
            elif cel.celebrity_type==u'导演':
                directors.append(cel)

        sql = "select u.* from movie_favorite mf left join users u on u.id=mf.user_id where mf.movie_id=:mid limit 10"
        favorites = conn.execute(text(sql),{'mid':mid})
        subjects = movie.subjects.all()
        articles = movie.articles.all()
    return render_template('movie/detail.html', movie=movie, form=form, cmform=cmform,favorites=favorites,subjects=subjects,
                               followers=followers, fbfm=fbfm, actors=actors, directors=directors, articles=articles)



@movie_page.route('/tags')
def tags():
    try:
        db = db_session()
        categories = Category.query.all()
        areas = Area.query.all()
        years = Year.query.all()
    finally:
        db.close()

    return render_template('movie/tags.html', categories=categories,areas=areas, years=years)

def sort_res(res,sort):
    if sort=='S':
        res = res.order_by(Movie.rating_num.desc())
    elif sort=='R':
        res = res.order_by(Movie.publish_date.desc())
    return res


@movie_page.route('/category/<ids>')
def category(ids):
    try:
        db = db_session()
        conn = db.connection()
        category_id = int(ids)
        keyword = request.args.get('keyword')
        page = int(request.args.get('page') or '1')
        PER_PAGE = 20
        offset = (page - 1) * PER_PAGE
        if category_id>0:
            res = Category.query.filter(Category.id==category_id)
            if not res.count()>0:
                abort(404)
            category = res.one()
            sort = request.args.get('sort') or ''
            res = category.movies
            # res = res.filter(Movie.duration>0)
            mres = sort_res(res,sort)
            count = mres.count()
            results=mres.limit(PER_PAGE).offset(offset)
        else:
            abort(404)
    finally:
        conn.close()
        db.close()

    pagination = Pagination(page, PER_PAGE, count)
    return render_template('movie/category.html', results=results,current_category=category,
                           keyword=keyword, pagination=pagination, current_sort_type=sort)


@movie_page.route('/area/<ids>')
def area(ids):
    try:
        db = db_session()
        conn = db.connection()
        area_id = int(ids)
        keyword = request.args.get('keyword')
        page = int(request.args.get('page') or '1')
        PER_PAGE = 20
        offset = (page - 1) * PER_PAGE
        if area_id>0:
            res = Area.query.filter(Area.id==area_id)
            if not res.count()>0:
                abort(404)
            area = res.one()
            sort = request.args.get('sort') or 'R'
            res = area.movies
            # res = res.filter(Movie.duration>0)
            mres = sort_res(res, sort)
            count = mres.count()
            results=mres.limit(PER_PAGE).offset(offset)
        else:
            abort(404)
    finally:
        conn.close()
        db.close()

    pagination = Pagination(page, PER_PAGE, count)
    return render_template('movie/area.html', results=results,current_area=area,
                           keyword=keyword, pagination=pagination, current_sort_type=sort)



@movie_page.route('/search/')
def search():
    keyword = request.args.get('keyword') or ''
    sort = request.args.get('sort') or 'O'
    page = int(request.args.get('page') or '1')
    PER_PAGE = 20
    offset = (page - 1) * PER_PAGE
    try:
        db = db_session()
        res = Movie.query

        if len(keyword)>0:
            words = ['%'+keyword+'%']
            rule = and_(*[Movie.name.like(w) for w in words])
            res = res.filter(rule)

        res = sort_res(res,sort)

        results = res.limit(PER_PAGE).offset(offset)
        count = res.count()
    finally:
        db.close()
    url = url_for('movie_page.search')+'?keyword='+keyword+'&sort='
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('movie/search.html', results=results, pagination=pagination, keyword=keyword, url=url, current_sort_type=sort)


@movie_page.route('/addbt/<mid>', methods=['GET', 'POST'])
def addbt(mid):
    print session
    print url_for('security.logout')
    if not 'username' in session:
            return redirect(url_for('user_page.login', url=url_for('movie_page.addbt', mid=mid)))
    movieres = db.query(Movie).filter(Movie.id==mid)
    if movieres.count()==0:
        abort(404)
    movie = movieres.first()
    form = BtForm(request.form)
    if request.method=='POST' and form.validate():
        bt = Bt(
                user_id=session['uid'],
                url= request.form['url'],
                title=request.form['title'],
                movie_id=mid,
                size = request.form['size'],
                format=request.form['format'],
                version=request.form['version'],
                status = u'正常'
            )
        db.add(bt)
        db.commit()
        if bt.id>0:
            movie.bt_count+=1
            db.commit()
            return redirect(url_for('bt_page.show', btid=bt.id))
    
    return render_template('movie/addbt.html', movie=movie, form=form)


@movie_page.route('/favorite/<mid>', methods=['POST'])
def favorite(mid):
    if not 'uid' in session:
        return jsonify({'status':2, 'info':'not login'})

    uid = session['uid']

    res = db.query(Movie).filter(Movie.id==mid)
    if res.count()==0:
        return jsonify({'status':3, 'info':'the movie is not exists'})

    movie = res.one()

    
    if movie.favorited():
        sql = "delete from movie_favorite where movie_id=:mid and user_id=:uid"
        conn.execute(text(sql),{
            'mid':mid,
            'uid':uid
            })
        movie.favorite_count-=1
    else:
        sql = "insert into movie_favorite set movie_id=:mid, user_id=:uid, created_at=:ca"
        conn.execute(text(sql),{
            'mid':mid,
            'uid':uid,
            'ca':now_datetime()
            })
        movie.favorite_count+=1
    db.commit()

    return jsonify({'status':1})
