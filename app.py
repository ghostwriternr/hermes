"""
Main flask process
"""
import json
import atexit
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bson import ObjectId

from mail import send_mail
from models import get_type_latest, get_all_latest

APP = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    """
    Class to convert ObjectId types to string
    """
    def default(self, o): # pylint: disable=E0202
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, bytes):
            return o.decode("utf-8")
        return json.JSONEncoder.default(self, o)

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
    notices = get_all_latest()
    notices = JSONEncoder().encode(notices)
    return jsonify(Notices=json.loads(notices))

@APP.route('/<string:noticeboard>', methods=['GET'])
def get_type(noticeboard):
    """
    Handle http request for specific type
    """
    notices = get_type_latest(noticeboard)
    notices = JSONEncoder().encode(notices)
    return jsonify(Notices=json.loads(notices))

if __name__ == "__main__":
    APP.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
