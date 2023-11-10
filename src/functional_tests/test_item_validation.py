from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        input_box = self.driver.find_element(By.ID, 'id_content')
        input_box.send_keys('')
        input_box.submit()
        self.wait_for(By.CSS_SELECTOR, '.errorlist')
