from wtforms import Form
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta

from flask import session


class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'EPj00jpfj8Gx1SjnyLxwBBSQfnQ9DJYe0Ym'
        csrf_time_limit = timedelta(minutes=20)

        @property
        def csrf_context(self):
            return session

