import logging
import pprint
import time
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class FunctionalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_to_do_page(self) -> None:
        self.browser.get('http://0.0.0.0:8080/')
        self.assertIn('To-Do', self.browser.title)

        welcome_text = self.browser.find_element(
            By.CLASS_NAME, 'welcome__text'
        ).text
        self.assertIn('To-Do', welcome_text)

        input_box = self.browser.find_element(By.ID, 'id_content')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter new item name',
        )

        self.add_to_table_and_check_item('item 1')
        self.add_to_table_and_check_item('item 2')

    def add_to_table_and_check_item(self, item: str, timeout: int = 1) -> None:
        input_box = self.browser.find_element(By.ID, 'id_content')
        input_box.send_keys(item)
        input_box.send_keys(Keys.ENTER)

        time.sleep(timeout)

        result_table = self.browser.find_element(By.CLASS_NAME, 'result_table')
        items = result_table.find_elements(By.TAG_NAME, 'td')

        self.assertTrue(any(i.text == item for i in items))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
