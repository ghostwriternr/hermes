# -*- coding: utf-8 -*-
"""
Module to manage sending emails
"""
from __future__ import print_function
from os import environ as env
from datetime import datetime
import requests

from scrapers import internal_scraper, public_scraper
from scrapers.settings import load_env

load_env()

REQUESTS_SESSION = requests.Session()

def get_attachment(attachment_url):
    """
    Return PDF given attachment URL
    """
    response = REQUESTS_SESSION.get(attachment_url)
    return response.content

def get_new_notices():
    """
    Fetch new notices from internal & public noticeboards
    """
    new_notices = internal_scraper.scrape_internal()
    new_notices['public'] = public_scraper.scrape_public()
    return new_notices

def send_mail():
    """
    Method to send mail
    """
    print(
        """
        **************************************
        %s
        **************************************
        """ % datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    )
    new_notices = get_new_notices()
    mailgun_base_url = 'https://api.mailgun.net/v3/%s' % env['MAILGUN_DOMAIN']
    data = {
        'from': (None, 'Hermes <no-reply@%s>' % env['MAILGUN_DOMAIN']),
        'fromname': (None, 'Hermes'),
        'to': (None, env['TARGET_EMAIL'])
    }

    for section in new_notices:
        for notice in new_notices[section]:
            files = []
            data['subject'] = (None, notice['title'])
            data['html'] = (None, notice['html'])
            if 'attachment' in notice:
                attachment_name = notice['attachment'].split('/')[-1]
                files = [('attachment', (attachment_name, get_attachment(notice['attachment'])))]
            print(data)
            response = REQUESTS_SESSION.post(
                mailgun_base_url + '/messages',
                data=data,
                auth=('api', env['MAILGUN_API_KEY']),
                files=files
            )
            print(response.text)

if __name__ == "__main__":
    send_mail()
