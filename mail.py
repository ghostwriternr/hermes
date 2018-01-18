"""
Module to manage sending emails
"""
from os import environ as env
import requests
from scrapers.internal_scraper import scrape_internal
from scrapers.public_scraper import scrape_public

from settings import load_env
load_env()

REQUESTS_SESSION = requests.Session()

def get_attachment(attachment_url):
    """
    Return PDF given attachment URL
    """
    response = REQUESTS_SESSION.get(attachment_url)
    return response.content

def send_mail():
    """
    Method to send mail
    """
    new_notices = scrape_internal()
    new_notices += scrape_public()
    mailgun_base_url = 'https://api.mailgun.net/v3/%s' % env['MAILGUN_DOMAIN']
    data = {
        'from': (None, 'Hermes <no-reply@%s>' % env['MAILGUN_DOMAIN']),
        'fromname': (None, 'Hermes'),
        'to': (None, 'ghostwriternr@gmail.com')
    }

    for section in new_notices:
        for notice in new_notices[section]:
            files = []
            data['subject'] = (None, notice['title'])
            data['text'] = (None, notice['text'])
            if 'attachment' in notice:
                attachment_name = notice['attachment'].split('/')[-1]
                files = [('attachment', (attachment_name, get_attachment(notice['attachment'])))]
            response = REQUESTS_SESSION.post(
                mailgun_base_url + '/messages',
                data=data,
                auth=('api', env['MAILGUN_API_KEY']),
                files=files
            )
            print(response.text)

if __name__ == "__main__":
    send_mail()
