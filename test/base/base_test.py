import unittest
from selenium import webdriver


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()  # TODO: Should be from conf/cmd line

    def tearDown(self):
        self.driver.quit()
