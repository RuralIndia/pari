import unittest
from selenium import webdriver


class Test(unittest.TestCase):

    def setup_method(self, method):
        self.driver = webdriver.Firefox()  # TODO: Should be from conf/cmd line

    def teardown_method(self, method):
        self.driver.quit()
