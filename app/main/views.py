from flask import request, render_template, redirect, url_for, jsonify

from app import app, db
from app.models import Users


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register", methods=["Post", "Get"])
def register():
    username = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if username and email and password:
        if Users.query.filter_by(email=email).first() and Users.query.filter_by(password=password):
            return redirect(url_for('publish'))

        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    msg = 'Проверте все поля!'
    return render_template('register.html', msg=msg)


@app.route("/login", methods=["Post", "Get"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        if Users.query.filter_by(email=email).first() and Users.query.filter_by(password=password):
            return redirect(url_for('publish'))

    msg = 'Проверте все поля!'
    return render_template('login.html', msg=msg)


@app.route('/publish')
def publish():
    return render_template('publish.html')

