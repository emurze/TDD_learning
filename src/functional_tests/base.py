from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from functional_tests.libs import MyLiveServerTestCase, get_driver


class FunctionalTest(MyLiveServerTestCase):
    def setUp(self) -> None:
        self.driver = get_driver()

        staging_server = os.getenv('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

        self.driver.get(self.live_server_url)
        self.register('vlad', '146080ce')

    def tearDown(self) -> None:
        self.driver.quit()

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

        username_input = self.driver.find_element(By.ID, 'id_username')
        password_input = self.driver.find_element(By.ID, 'id_password')
        password2_input = self.driver.find_element(By.ID, 'id_password2')

        username_input.send_keys(username)
        password_input.send_keys(password)
        password2_input.send_keys(password)
        password2_input.submit()