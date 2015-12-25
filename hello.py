import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/google-adwords/oauth2callback')
def hello_ggl():
    return 'Hello Google!'
