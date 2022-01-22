#!/usr/bin/env python3
import os
import sqlite3
from pathlib import Path

from flask import Flask, g, redirect, request

import libsession
from mod_api import mod_api
from mod_csp import mod_csp
from mod_hello import mod_hello
from mod_mfa import mod_mfa
from mod_posts import mod_posts
from mod_user import mod_user

application = Flask(__name__)
application.config['SECRET_KEY'] = 'aaaaaaa'

application.register_blueprint(mod_hello, url_prefix='/hello')
application.register_blueprint(mod_user, url_prefix='/user')
application.register_blueprint(mod_posts, url_prefix='/posts')
application.register_blueprint(mod_mfa, url_prefix='/mfa')
application.register_blueprint(mod_csp, url_prefix='/csp')
application.register_blueprint(mod_api, url_prefix='/api')

csp_file = Path('csp.txt')
csp = ''

if csp_file.is_file():
    with csp_file.open() as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line = line.replace('\n', '')
            if line:
                csp += line
if csp:
    print('CSP:', csp)


@application.route('/')
def do_home():
    return redirect('/posts')

@application.before_request
def before_request():
    g.session = libsession.load(request)

@application.after_request
def add_csp_headers(response):
    if csp:
        response.headers['Content-Security-Policy'] = csp
    return response


application.run(debug=True, host='127.0.0.1', port=443, extra_files='csp.txt')
