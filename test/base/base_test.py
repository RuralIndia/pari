import unittest
from selenium import webdriver


class Test(unittest.TestCase):
    
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        
    def teardown_method(self, method):
        self.driver.quit()