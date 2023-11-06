from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from functional_tests.my_live_server_test import MyLiveServerTestCase
from functional_tests.selenium_driver import get_driver


class FunctionalTest(MyLiveServerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.driver = get_driver()
        self.driver.get(self.live_server_url)

    def tearDown(self) -> None:
        super().tearDown()
        self.driver.quit()

    def test_home_page_title(self) -> None:
        """User history"""
        self.assertIn('To-Do', self.driver.title)

    def test_todo_input_box(self) -> None:
        input_box = self.driver.find_element(By.ID, 'id_content')
        input_box.send_keys('item_100')
        input_box.submit()

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.ID, "todo_list"),
            )
        )
        elem = self.driver.find_element(By.ID, "todo_list")
        self.assertIn('item_1', elem.text)
