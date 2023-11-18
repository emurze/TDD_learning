from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self) -> None:
        self.driver.set_window_size(1024, 768)
        input_box = self.get_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=50,
        )
