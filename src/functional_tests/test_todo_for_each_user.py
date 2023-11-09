import time

from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from functional_tests.libs import get_driver


class TodoForEachUserTest(FunctionalTest):
    def test_unique_todo_list(self) -> None:
        """Vlad go to the page """
        input_box = self.driver.find_element(By.ID, 'id_content')
        input_box.send_keys('PARTY1')
        input_box.submit()

        current_url = self.driver.current_url
        self.assertRegex(current_url, '/lists/.+')

        todo_list = self.get_todo_list()
        self.assertIn('PARTY1', todo_list.text)
        self.driver.quit()

        """Lera go to the page"""
        self.driver = get_driver()
        self.driver.get(self.live_server_url)
        self.register('vlad2', '146080ce')

        time.sleep(1)

        input_box = self.driver.find_element(By.ID, 'id_content')
        input_box.send_keys('PARTY2')
        input_box.submit()

        todo_list = self.get_todo_list()

        self.assertNotIn('PARTY1', todo_list.text)
        self.assertIn('PARTY2', todo_list.text)
