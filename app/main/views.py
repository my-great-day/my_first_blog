from flask import request, render_template, redirect, url_for, jsonify, session
from sqlalchemy.sql.functions import current_user

from app import app, db
from app.models import Users, Publish, Comment


@app.route('/')
def index():
    if session.get('my_first_blog'):
        session.pop('my_first_blog')
    return render_template('index.html')


@app.route("/register", methods=["Post", "Get"])
def register():
    if session.get('my_first_blog'):
        session.pop('my_first_blog')
    username = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if username and email and password:
        session["my_first_blog"] = email
        if Users.query.filter_by(email=email).first() and Users.query.filter_by(password=password):
            return redirect(url_for('publish', id=email))

        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    msg = 'Проверте все поля!'
    return render_template('register.html', msg=msg)


@app.route("/login", methods=["Post", "Get"])
def login():
    if session.get('my_first_blog'):
        session.pop('my_first_blog')
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        if Users.query.filter_by(email=email).first() and Users.query.filter_by(password=password):
            session["my_first_blog"] = email
            return redirect(url_for('publish', id=email))

    msg = 'Проверте все поля!'
    return render_template('login.html', msg=msg)


@app.route('/publish/<id>')
def publish(id):
    if session.get('my_first_blog') != id:
        return redirect(url_for('register'))
    pub = Publish.query.all()
    return render_template('publish.html', id_url=id, pub=pub, user=Users)


@app.route('/create_publish/<id>', methods=['POST', 'GET'])
def create_publish(id):
    if session.get('my_first_blog') != id:
        return redirect(url_for('register'))
    msg = ''
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        if not text and not title:
            msg = 'Поля не должен быт пустым!'
        else:
            user = Users.query.filter_by(email=id).first()
            pub = Publish(title_article=title, text_article=text, users_id=user.id)
            db.session.add(pub)
            db.session.commit()

            return redirect(url_for('publish', id=id))
    return render_template('create_publish.html', msg=msg)


@app.route('/my_publish/<id>')
def my_publish(id):
    if session.get('my_first_blog') != id:
        return redirect(url_for('register'))
    user = Users.query.filter_by(email=id).first()
    pub = Publish.query.filter_by(users_id=user.id).all()
    return render_template('my_publish.html', id_url=id, my_pub=pub)


@app.route('/delete/<user>/<id>')
def delete(user, id):
    if session.get('my_first_blog') == user:
        comp = Publish.query.filter_by(id=int(id)).first()
        db.session.delete(comp)
        db.session.commit()
        return redirect(url_for('.my_publish', id=user))
    return redirect(url_for('ups'))


@app.route('/create_comment/<user>/<id_user>/<id_pub>', methods=['Post', 'Get'])
def create_comment(user, id_user, id_pub):
    if session.get('my_first_blog') == user:
        if request.method == 'POST':
            com = request.form.get('comment')
            if com:
                comment = Comment(comment=com, users_id=id_user, publish_id=id_pub)
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('publish', id=user))

    return redirect(url_for('ups'))


@app.route('/ups/blablabla')
def ups():
    return 'Ошибка страниц!'
