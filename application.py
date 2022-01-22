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



@application.route('/')
def do_home():
    return redirect('/posts')

@application.before_request
def before_request():
    g.session = libsession.load(request)



