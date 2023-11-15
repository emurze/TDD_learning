from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class SendMailTest(FunctionalTest):
    def test_button(self) -> None:
        self.driver.get(self.live_server_url)
        self.assertIn('To-Do', self.driver.title)

        email_input = self.driver.find_element(By.ID, 'id_email')
        email_input.send_keys('adm1@adm1.com')
        email_input.submit()

        self.assertIn(
            'Email message was successfully sent',
            self.driver.page_source,
        )
