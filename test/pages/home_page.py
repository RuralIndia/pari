from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from test.base import Page


class HomePage(Page):

    URL = "http://127.0.0.1:8000"  # TODO: Should be from conf

    search_box = (By.CSS_SELECTOR, "input.search-query")  # TODO: Try wrapping it in a decorator and do action based on the element type

    def __int__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self

    def wait_for_loading(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.find_element(*self.search_box))
        return self
