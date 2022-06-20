from flask import Flask, jsonify
from app import blog


@blog.route("/")
def index():
    return jsonify('Hello')
