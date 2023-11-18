import time

from django.core import mail
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest

email_to = 'adm1@adm1.com'


class SendMailTest(FunctionalTest):
    def test_button(self) -> None:
        self.driver.get(self.live_server_url)
        self.assertIn('To-Do', self.driver.title)

        email_input = self.driver.find_element(By.ID, 'id_email')
        email_input.send_keys(email_to)

        submit = self.driver.find_element(
            By.CSS_SELECTOR,
            '#email_form button[type="submit"]',
        )
        submit.click()

        time.sleep(1)

        self.assertIn(email_to, mail.outbox[0].to)
