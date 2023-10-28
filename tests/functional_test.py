import logging
from pprint import pprint

from selenium import webdriver

lg = logging.getLogger(__name__)

PROTOCOL = 'http'
SOCKET = '0.0.0.0:8080'

with webdriver.Firefox() as browser:
    browser.get(f'{PROTOCOL}://{SOCKET}')

    assert 'successfully' in browser.title

    pprint(help(browser))
