import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from functional_tests.libs import MyLiveServerTestCase, get_driver


class FunctionalTest(MyLiveServerTestCase):
    def setUp(self) -> None:
        self.driver = get_driver()
        self.driver.get(self.live_server_url)
        self.register('vlad', '146080ce')

    def tearDown(self) -> None:
        self.driver.quit()

    def test_home_page_title(self) -> None:
        self.assertIn('To-Do', self.driver.title)

    def test_todo_input_box(self) -> None:
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

    def get_todo_list(self) -> WebElement:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.ID, "todo_list"),
            )
        )
        elem = self.driver.find_element(By.ID, "todo_list")
        return elem

    def register(self, username: str, password: str) -> None:
        self.driver.get(self.live_server_url + '/register/')

        print('hehe')

        username_input = self.driver.find_element(By.ID, 'id_username')
        password_input = self.driver.find_element(By.ID, 'id_password')
        password2_input = self.driver.find_element(By.ID, 'id_password2')

        print(username_input)
        print(password_input)
        print(password2_input)

        username_input.send_keys(username)
        password_input.send_keys(password)
        password2_input.send_keys(password)
        password2_input.submit()
