"""
Main flask process
"""
import atexit
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from mail import send_mail, get_new_notices

APP = Flask(__name__)

SCHEDULER = BackgroundScheduler()
SCHEDULER.start()
SCHEDULER.add_job(
    func=send_mail,
    trigger=IntervalTrigger(minutes=1),
    id='scraper_job',
    name='Poll IIT KGP\'s internal noticeboards every one minute',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: SCHEDULER.shutdown())

@APP.route('/')
def index():
    """
    Handle http request to root
    """
    return jsonify(Notices=get_new_notices())

if __name__ == "__main__":
    APP.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
