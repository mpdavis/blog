import json

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import flask_login
from flask_login import login_required

from mongoengine.queryset import DoesNotExist

from blog.admin.models import GlobalSettings

from blog import db

from blog.auth import UserAwareMethodView
from blog.auth import setup_incomplete
from blog.auth.forms import LoginForm
from blog.auth.forms import SetupForm
from blog.auth.models import User


auth = Blueprint('auth', __name__, template_folder='templates')


class LoginView(UserAwareMethodView):
    active_nav = 'login'

    def get(self):
        form = LoginForm()
        return render_template('auth/login.html', form=form)

    def post(self):
        form = LoginForm(request.form)

        if form.validate():

            try:
                user = User.objects.get(username=form.username.data)
            except DoesNotExist, e:
                user = None

            if user and user.check_password(form.password.data):
                flask_login.login_user(user)
                return redirect(url_for("admin.index"))

            flash("Invalid Username or Password")

        context = self.get_context(form=form)
        return render_template('auth/login.html', **context)


class LogoutView(UserAwareMethodView):
    decorators = [login_required]

    def get(self):
        flask_login.logout_user()
        return redirect(url_for('posts.list'))


class SetupView(UserAwareMethodView):
    decorators = [setup_incomplete]

    def get(self):
        form = SetupForm()
        return render_template('auth/setup.html', form=form)

    def post(self):
        form = SetupForm(request.form)

        if form.validate():

            global_settings = GlobalSettings.get_global_settings_object()

            import logging
            logging.warn(global_settings)

            if form.disqus_shortname.data:
                global_settings.disqus_shortname = form.disqus_shortname.data

            if form.flog_name.data:
                global_settings.flog_name = form.flog_name.data

            if form.author_name.data:
                global_settings.author_name = form.author_name.data

            if form.author_bio.data:
                global_settings.author_bio = form.author_bio.data

            db.session.commit()

            username = form.username.data
            password = User.hash_password(form.password.data)

            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user)

            return redirect(url_for('admin.add-post'))

        return redirect(url_for('admin.add-post'))


# Register the urls
auth.add_url_rule('/login/', view_func=LoginView.as_view('login'))
auth.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))
auth.add_url_rule('/setup/', view_func=SetupView.as_view('setup'))
