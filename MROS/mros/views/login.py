from flask import Flask, render_template, request, redirect, session, Blueprint
from mros.tools.db_helper import SQLHelper
from wtforms import Form
from wtforms.fields import simple
from wtforms.fields import html5
from wtforms.fields import core
from wtforms import widgets
from wtforms import validators
import functools

account = Blueprint('login', __name__, url_prefix='/account')

# 1.加载的时候创建类，Form类的
# 2.类里边实例化字段对象


class LoginForm(Form):
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空')
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'}
    )

    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )


@account.route('/', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(formdata=request.form)
        if form.validate():
            args = [form.data['name'],form.data['pwd']]
            mysql = 'SELECT * from user WHERE NAME = %s AND password = %s'
            val = SQLHelper.fetch_one(mysql,args)

            if val:
                session['user_id'] = val['uid']
                return redirect('/index')

            return 'login....'
        return render_template('login.html', form=form)
