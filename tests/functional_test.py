"""
Check main page title. It should work.
Additionally, It should contain successfully.

1. Client can't see the site

End of this User History

"""

import logging
import time
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

lg = logging.getLogger(__name__)

PROTOCOL = 'http'
SOCKET = '0.0.0.0:8080'
URL = f'{PROTOCOL}://{SOCKET}'


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self) -> None:
        self.browser.get(URL)

        # Client notices that title should contain To-Do
        self.assertIn('To-Do', self.browser.title)

        # And also welcome should contain 'To-Do'
        welcome_text = self.browser.find_element(
            by=By.CLASS_NAME,
            value='welcome__text'
        ).text
        self.assertIn('To-Do', welcome_text)

        # Client desire to see input with the definite inner message
        input_box = self.browser.find_element(
            by=By.ID,
            value='id_new_item'
        )
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item',
        )

        input_box_message = 'Vlad gay'

        # Client desire to send message
        input_box.send_keys(input_box_message)

        # And click the submit button
        input_box.send_keys(Keys.ENTER)

        # Wait for reloading should be replaced on async wait
        # in the near future
        time.sleep(1)

        # Then client desire to see the result table
        table = self.browser.find_element(by=By.ID, value='id_item_table')
        items = table.find_elements(by=By.TAG_NAME, value='tr')

        # With the entered message
        self.assertTrue(any(item == input_box_message for item in items))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
