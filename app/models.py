from datetime import datetime
from time import strftime

from app import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.VARCHAR(255), default='Guests', nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(100), nullable=False)
    publish = db.relationship('Publish', backref='users', passive_deletes=True)
    comment = db.relationship('Comment', backref='users', passive_deletes=True)
    like = db.relationship('Like', backref='users', passive_deletes=True)
    look = db.relationship('Look', backref='users', passive_deletes=True)


class Publish(db.Model):
    __tablename__ = 'publish'
    id = db.Column(db.Integer(), primary_key=True)
    title_article = db.Column(db.VARCHAR(255), default='No name')
    text_article = db.Column(db.String(), default='Coming soon!')
    create_on = db.Column(db.DateTime(), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    users_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    comment_id = db.relationship('Comment', backref='publish', passive_deletes=True)
    like_id = db.relationship('Like', backref='publish', passive_deletes=True)
    look_id = db.relationship('Look', backref='publish', passive_deletes=True)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(), nullable=False)
    create_on = db.Column(db.DateTime(), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    users_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    publish_id = db.Column(db.Integer(), db.ForeignKey('publish.id', ondelete='CASCADE'), nullable=False)


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer(), primary_key=True)
    total = db.Column(db.Integer(), nullable=False)
    create_on = db.Column(db.DateTime(), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    users_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    publish_id = db.Column(db.Integer(), db.ForeignKey('publish.id', ondelete='CASCADE'), nullable=False)


class Look(db.Model):
    __tablename__ = 'look'
    id = db.Column(db.Integer(), primary_key=True)
    total = db.Column(db.Integer(), nullable=False)
    create_on = db.Column(db.DateTime(), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    users_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    publish_id = db.Column(db.Integer(), db.ForeignKey('publish.id', ondelete='CASCADE'), nullable=False)
