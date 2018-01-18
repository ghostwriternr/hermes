"""
Main flask process
"""
import atexit
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ug_scraper import scrape
from mail import send_mail

APP = Flask(__name__)

SCHEDULER = BackgroundScheduler()
SCHEDULER.start()
SCHEDULER.add_job(
    func=send_mail,
    trigger=IntervalTrigger(seconds=5),
    id='scraper_job',
    name='Scrape ug noticeboard every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: SCHEDULER.shutdown())

@APP.route('/')
def index():
    return jsonify(Notices=scrape())

if __name__ == "__main__":
    APP.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
