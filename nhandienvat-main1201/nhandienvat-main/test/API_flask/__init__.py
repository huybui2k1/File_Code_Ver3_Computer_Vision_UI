from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)
    return app