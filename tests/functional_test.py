"""
Check main page title. It should work.
Additionally, It should contain successfully.

1. Client can't see the site

End of this User History

"""

import logging
import unittest

from selenium import webdriver

lg = logging.getLogger(__name__)

PROTOCOL = 'http'
SOCKET = '0.0.0.0:8080'


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(f'{PROTOCOL}://{SOCKET}')

        self.assertIn('install', self.browser.title)

        self.fail(f'Browser title was {self.browser.title}')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
