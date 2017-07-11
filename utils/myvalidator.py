#coding=utf-8

from db.Orms import db_, User

class ValidationError(ValueError):
    """
    Raised when a validator fails to validate its input.
    """
    def __init__(self, message='', *args, **kwargs):
        ValueError.__init__(self, message, *args, **kwargs)


class StopValidation(Exception):
    """
    Causes the validation chain to stop.

    If StopValidation is raised, no more validators in the validation chain are
    called. If raised with a message, the message will be added to the errors
    list.
    """
    def __init__(self, message='', *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)


class UniqueUsername(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
	res = User.query.filter(User.name==field.data)
	if res.count()>0:
            message = self.message
            if message is None:
                message = field.gettext(u'用户名“' + field.data + u'”已存在')
                raise ValidationError(message)


class UniqueEmail(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
	res = User.query.filter(User.email==field.data)
	if res.count()>0:
            message = self.message
            if message is None:
                message = field.gettext(u'邮箱“' + field.data + u'”已存在')
                raise ValidationError(message)


unique_username = UniqueUsername
unique_email = UniqueEmail
