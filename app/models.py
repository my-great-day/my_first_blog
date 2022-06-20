from datetime import datetime

from app import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.VARCHAR(255), default='Guests', nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(100), nullable=False)


class Publish(db.Model):
    __tablename__ = 'publish'
    id = db.Column(db.Integer(), primary_key=True)
    title_article = db.Column(db.VARCHAR(255), default='No name')
    text_article = db.Column(db.String(), default='Coming soon!')
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
