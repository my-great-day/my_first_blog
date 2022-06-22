from flask import request, jsonify

from app import api, db, jwt
from app.models import Users

from flask_jwt_extended import jwt_required, current_user, create_access_token


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()


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


@api.route("/get_res", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        user=current_user.username,
        email=current_user.email
    )
