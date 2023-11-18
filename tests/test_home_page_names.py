from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class HomePageNamesTest(FunctionalTest):
    def test_home_page_title(self) -> None:
        self.assertIn('To-Do', self.driver.title)

    def test_input_box_placeholder(self) -> None:
        input_box = self.get_input_box()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
