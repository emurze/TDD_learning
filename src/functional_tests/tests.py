import time
import unittest

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from functional_tests.my_live_server_test import MyLiveServerTestCase
from functional_tests.selenium_driver import get_driver


class FunctionalTest(MyLiveServerTestCase):
    def setUp(self) -> None:
        self.driver = get_driver()

    def tearDown(self) -> None:
        self.driver.quit()

    def test_to_do_page(self) -> None:
        self.driver.get(self.live_server_url)

        self.assertIn('To-Do', self.driver.title)

        welcome_text = self.driver.find_element(
            By.CLASS_NAME, 'welcome__text'
        ).text
        self.assertIn('To-Do', welcome_text)

        input_box = self.driver.find_element(By.ID, 'id_content')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter new item name',
        )

        self.add_to_table_and_check_item('item 1')
        self.add_to_table_and_check_item('item 2')

    def add_to_table_and_check_item(self, item: str, timeout: int = 1) -> None:
        input_box = self.driver.find_element(By.ID, 'id_content')
        input_box.send_keys(item)
        input_box.send_keys(Keys.ENTER)

        time.sleep(timeout)

        result_table = self.driver.find_element(By.CLASS_NAME, 'result_table')
        items = result_table.find_elements(By.TAG_NAME, 'td')

        self.assertTrue(any(i.text == item for i in items))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
