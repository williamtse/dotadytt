# -*- coding: UTF-8 -*-
from models.BaseForm import BaseForm
from wtforms import PasswordField, StringField, HiddenField,SubmitField
from utils.myvalidator import unique_username, unique_email
from wtforms.validators import length,equal_to,required,email,regexp

class SignupForm(BaseForm):
    username = StringField(u'用户名', [length(min=4,max=30,message=u"输入至少4位字符"),
                            unique_username(),
                            required()
                            ,regexp('^[a-zA-Z]{1}[0-9a-zA-Z_]*$',
                                    message=u'请输入以字母开头的字母、数字和下划线的组合')])
    password = PasswordField(u'密码',[length(min=6, max=128,message=u"至少输入6位密码"),required()])
    confirm = PasswordField(u'再次输入密码',[equal_to('password',u'两次输入密码不一致')])
    email = StringField(u'邮箱',[email(message=u"邮箱格式错误"),required(),unique_email()])
    submit = SubmitField(u'注册')
    hidden_tag = HiddenField()
    error = ''

