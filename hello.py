import os
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/google-adwords/oauth2callback')
def hello_ggl():
    error = request.args.get('error','') 
    if error != '':
    	return "Google returned the following error: " + error
    code = request.args.get('code','')
    ret_str = 'Hello Google! Your code is ' + code
    return ret_str