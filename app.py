# -*- coding: utf-8 -*-
"""
Main flask process
"""
from os import environ as env
import json
import atexit
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import requests

from mail import send_mail
from scrapers.settings import load_env

load_env()

APP = Flask(__name__)
REQUESTS_SESSION = requests.Session()

SCHEDULER = BackgroundScheduler()
SCHEDULER.start()
SCHEDULER.add_job(
    func=send_mail,
    trigger=IntervalTrigger(minutes=1),
    id='send_mail',
    name='Poll IIT KGP\'s noticeboards every minute',
    replace_existing=True)
atexit.register(lambda: SCHEDULER.shutdown()) # pylint: disable=W0108

@APP.route('/', methods=['GET'])
def index():
    """
    Handle http request to root
    """
    notices = REQUESTS_SESSION.get(env['VERITAS_URL'])
    return jsonify(notices.json())

@APP.route('/<string:noticeboard>', methods=['GET'])
def get_type(noticeboard):
    """
    Handle http request for specific type
    """
    notices = REQUESTS_SESSION.get(env['VERITAS_URL'] + noticeboard)
    return jsonify(notices.json())

if __name__ == "__main__":
    APP.run(debug=True, host='0.0.0.0', port=5010, use_reloader=False)
