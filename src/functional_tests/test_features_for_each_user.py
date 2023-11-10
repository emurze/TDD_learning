import time

from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from functional_tests.libs import get_driver


class FeaturesForEachUserTest(FunctionalTest):
    def test_each_user_unique_list(self) -> None:
        """Vlad go to the page """
        input_box = self.get_input_box()
        input_box.send_keys('PARTY1')
        input_box.submit()

        current_url = self.driver.current_url
        self.assertRegex(current_url, '/lists/.+')

        todo_list = self.wait_todo_list()
        self.assertIn('PARTY1', todo_list.text)
        self.driver.quit()

        """Lera go to the page"""
        self.driver = get_driver()
        self.driver.get(self.live_server_url)
        self.register('vlad2', '146080ce')

        input_box = self.get_input_box()
        input_box.send_keys('PARTY2')
        input_box.submit()

        todo_list = self.wait_todo_list()
        self.assertNotIn('PARTY1', todo_list.text)
        self.assertIn('PARTY2', todo_list.text)
