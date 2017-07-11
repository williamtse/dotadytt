#coding=utf-8
from BaseView import BaseView
from flask_admin import expose
from admin.form.CategoryCreateForm import CategoryCreateForm
from flask import request,redirect
from db.Orms import Category
from db.database import db_session

db = db_session()

class CategoryView(BaseView):
    form_excluded_columns = ['movies']

    @expose('/new/', methods=['GET', 'POST'])
    def create_view(self):
        form = CategoryCreateForm(request.form)
        if request.method == 'POST' and form.validate():
            cate = Category(name=request.form['name'])
            db.add(cate)
            db.commit()
            if cate.id:
                return redirect(request.args.get('url'))
        return self.render('admin/create_category.html', form=form)