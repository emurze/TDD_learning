from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class HomePageNamesTest(FunctionalTest):
    def test_home_page_title(self) -> None:
        self.assertIn('To-Do', self.driver.title)

    def test_input_box(self) -> None:
        input_box = self.driver.find_element(By.ID, 'id_content')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
