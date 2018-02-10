"""
Scraper for IITKGP internal notice boards
http://noticeboard.iitkgp.ernet.in/
"""
from os import path, environ as env
import json
from urllib.parse import urljoin
import hashlib
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

if __package__ is None:
    import sys
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from settings import load_env # pylint: disable-msg=E0611
else:
    from .settings import load_env

load_env()

MC = MongoClient(env['MONGODB_URI'])
REQUESTS_SESSION = requests.Session()
DIFF_NOTICES = 10

BASE_URL = 'http://noticeboard.iitkgp.ernet.in/'
SUB_URLS = [
    'acad_ug/',
    'acad_pg/',
    'bcrth/'
]

def scrape_notice(notice_url, section, notice_has_attachment):
    """
    Scrape method for each notice
    """
    requests_response = REQUESTS_SESSION.get(notice_url)
    soup = BeautifulSoup(requests_response.text, "html.parser")
    notice = soup.find_all('tr')
    notice_details = notice[0].find_all('td')
    notice_title = notice_details[0].get_text()
    notice_time = notice_details[1].get_text()
    notice_html = notice[1].find('div')
    notice_text = notice[1].find('div').get_text()
    notice_json = {}
    notice_json['title'] = notice_title
    notice_json['time'] = notice_time.strip()
    notice_json['text'] = notice_text
    notice_json['html'] = str(notice_html)
    hash_md5 = hashlib.md5()
    if notice_has_attachment:
        notice_attachment = notice[1].find('a').get('href')
        notice_json['attachment'] = BASE_URL + section + notice_attachment
        attachment_response = REQUESTS_SESSION.get(notice_json['attachment'], stream=True)
        attachment_response.raw.decode_content = True
        for chunk in iter(lambda: attachment_response.raw.read(4096), b""):
            hash_md5.update(chunk)
        notice_json['attachment_md5'] = hash_md5.hexdigest()
    return notice_json

def handle_notices_diff(section, notices):
    """
    Method to check for new/updated notices
    """
    section = section.split('/')[0]
    new_notices = REQUESTS_SESSION.post(urljoin(env['VERITAS_URL'], "diff/" + section), json=notices)
    new_notices = json.loads(new_notices.json())
    return new_notices

def scrape_noticeboard(section):
    """
    Scrape method for selected noticeboard section
    """
    requests_response = REQUESTS_SESSION.get(BASE_URL + section)
    soup = BeautifulSoup(requests_response.text, "html.parser")
    notices = []
    diffed_notices = 0
    page_number = 1
    while True:
        print("Currently at page ", page_number)
        noticeboard = soup.find('td', {'valign': 'top'}).find('table')
        all_notices = noticeboard.find_all('tr')
        for notice in all_notices:
            notice_columns = notice.find_all('td')
            if len(notice_columns) == 3:
                notice_has_attachment = not notice_columns[1].find('a', {'class': 'notice'}) is None
                notice_url = notice_columns[2].find('a').get('href')
                notice_url = BASE_URL + section + notice_url
                notice_json = scrape_notice(notice_url, section, notice_has_attachment)
                notices.append(notice_json)
                diffed_notices += 1
                if env['FIRST_RUN'] == 'false' and diffed_notices == DIFF_NOTICES:
                    new_notices = handle_notices_diff(section, notices)
                    print("Found %d new notices in %s (%d checked)" % (
                        len(new_notices), section.split('/')[0], diffed_notices))
                    return new_notices
        try:
            next_page = all_notices[-1].find(
                'font', {'class': 'text'}).find('a', {'class': 'notice'})
            next_page_url = next_page.get('href')
            page_number += 1
            soup = BeautifulSoup(REQUESTS_SESSION.get(
                urljoin(BASE_URL, next_page_url)).text, "html.parser")
        except AttributeError:
            break
    new_notices = handle_notices_diff(section, notices)
    print("Found %d new notices in %s (%d checked)" % (
        len(new_notices), section.split('/')[0], diffed_notices))
    print(new_notices)
    return new_notices

def scrape_internal():
    """
    Scrape method for all noticeboard sections
    """
    print("Beginning to scrape internal noticeboards")
    new_notices = {}
    for section in SUB_URLS:
        print("Scraping %s" % section.split('/')[0])
        section_notices = scrape_noticeboard(section)
        new_notices[section.split('/')[0]] = section_notices
    return new_notices

if __name__ == "__main__":
    scrape_internal()
