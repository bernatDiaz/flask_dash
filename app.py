import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_manager, login_required, logout_user, login_user, current_user
from werkzeug.urls import url_parse

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

from models import User
from forms import SignupForm, LoginForm

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/hidden-plot/')
login_manager = LoginManager()
login_manager.init_app(server)

def protect_views(app):
    for view_func in app.server.view_functions:
        if view_func.startswith(app.config["url_base_pathname"]):
            app.server.view_functions[view_func] = login_required(app.server.view_functions[view_func])
    return app

app = protect_views(app)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
server.secret_key = 'asdfghijklmnopqrstu'
server.config['MYSQL_HOST'] = 'remotemysql.com'
server.config['MYSQL_USER'] = 'CjCNFuXROa'
server.config['MYSQL_PASSWORD'] = 'bMaWoiEpBj'
server.config['MYSQL_DB'] = 'CjCNFuXROa'

mysql = MySQL(server)

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (int(user_id),))
    account = cursor.fetchone()
    mysql.connection.commit()
    if(account):
        return User(account["username"],account["email"], account["password"], user_id)
    else:
        return None

@server.route('/plot/')
@login_required
def plot():
    return flask.redirect('/hidden-plot/')

@server.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)


@server.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        mysql.connection.commit()
        if account is not None:
            user = User(account.username, account.email, account.password, account.id)
            if user.check_password(form.password):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
    return render_template('login_form.html', form=form)

@server.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            print("account already exists")
            mysql.connection.commit()
        else:
            user = User(username,email,password)
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            id = mysql.connection.insert_id()
            user.set_id(id)

            mysql.connection.commit()
            login_user(user, remember=True)

            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('index'))

    return render_template("signup_form.html", form=form)

@server.route('/logout/')
def logout():
   logout_user()
   return redirect(url_for('login'))

login_manager.login_view = "login"