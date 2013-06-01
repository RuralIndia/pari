from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from test.base import Page
from .home_page import HomePage


class AdminPage(Page):

    URL = "%s/admin" % HomePage.URL  # TODO: Should be from conf

    user_name = (By.CSS_SELECTOR, "#id_username")  # TODO: Try wrapping it in a decorator and do action based on the element type

    def __int__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self

    def wait_for_loading(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.find_element(*self.user_name))
        return self
