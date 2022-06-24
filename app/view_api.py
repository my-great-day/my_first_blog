from flask import request, jsonify

from app import api, db, jwt
from app.models import Users, Like, Look, Publish, Comment

from flask_jwt_extended import jwt_required, current_user, create_access_token


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()


# Регистрация
@api.route("/registration", methods=["POST"])
def registration():
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("username", None)

    if Users.query.filter_by(email=email).first() and Users.query.filter_by(password=password):
        return jsonify(
            "У вас уже имеется аккаунт!",
            "Переходите на страницу логин чтобы получат токен!"
        )

    user = Users(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        "Ваш аккаунт добавлено!",
        "Переходите на страницу логин чтобы получат токен!"
    )


# Вход
@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("username", None)

    email = Users.query.filter_by(email=email).one_or_none()
    password = Users.query.filter_by(password=password).one_or_none()
    if not email and not password:
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


# Все посты
@api.route('/all_publish', methods=['Get'])
@jwt_required()
def all_publish():
    pub = []
    publish = Publish.query.all()
    for p in publish:
        user = Users.query.filter_by(id=p.users_id).first()
        pub.append({'title_article': p.title_article, 'text_article': f'{p.text_article[:30]}...',
                    'create_on': p.create_on.strftime("%Y-%m-%d %H:%M:%S"), 'username': user.username})
    return jsonify(
        publish=pub
    )


# Каждый пост по отделностю
@api.route('/read_publish', methods=['Get'])
@jwt_required()
def read_publish():
    try:
        comment = []
        read_publish_id = request.json.get('publish_id', None)
        publish = Publish.query.filter_by(id=read_publish_id).first()
        user = Users.query.filter_by(id=publish.users_id).first()

        comments = Comment.query.filter_by(publish_id=read_publish_id).all()
        like = Like.query.filter_by(publish_id=read_publish_id).first()
        look = Look.query.filter_by(publish_id=read_publish_id).first()

        for c in comments:
            user = Users.query.filter_by(id=c.users_id).first()
            comment.append({'username': user.username, 'comment': c.comment,
                            'date': c.create_on.strftime("%Y-%m-%d %H:%M:%S")})

        return jsonify(
            user=user.username,
            id=publish.id,
            title=publish.title_article,
            post=publish.text_article,
            date=publish.create_on.strftime("%Y-%m-%d %H:%M:%S"),
            comment=comment,
            like=like.total,
            look=look.total
        )
    except AttributeError:
        return jsonify(
            user=user.username,
            id=publish.id,
            title=publish.title_article,
            post=publish.text_article,
            date=publish.create_on.strftime("%Y-%m-%d %H:%M:%S"),
            comment=comment,
        )
