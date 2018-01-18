"""
Scraper for the UG Notice board
"""
from bs4 import BeautifulSoup
import requests

BASE_URL = 'http://noticeboard.iitkgp.ernet.in/acad_ug/'

def scrape_notice(notice_url):
    """
    Scrape method for each notice
    """
    requests_response = requests.get(notice_url)
    soup = BeautifulSoup(requests_response.text, "html.parser")
    notice = soup.find_all('tr')
    notice_details = notice[0].find_all('td')
    notice_title = notice_details[0].get_text()
    notice_time = notice_details[1].get_text()
    notice_text = notice[1].find('div').get_text()
    notice_attachment = notice[1].find('a').get('href')
    notice_json = {}
    notice_json['title'] = notice_title
    notice_json['time'] = notice_time.strip()
    notice_json['text'] = notice_text
    notice_json['attachment'] = BASE_URL + notice_attachment
    return notice_json

def scrape():
    """
    Scrape method for main noticeboard
    """
    requests_response = requests.get(BASE_URL)
    soup = BeautifulSoup(requests_response.text, "html.parser")
    noticeboard = soup.find('td', {'valign': 'top'}).find('table')
    all_notices = noticeboard.find_all('tr')
    notices = []
    for notice in all_notices:
        notice_columns = notice.find_all('td')
        if len(notice_columns) == 3:
            # notice_time = notice_columns[0].get_text()
            notice_url = notice_columns[2].find('a').get('href')
            notice_url = BASE_URL + notice_url
            notice_json = scrape_notice(notice_url)
            notices.append(notice_json)
    return notices

if __name__ == "__main__":
    scrape()
