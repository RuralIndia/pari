from test.base import Test
from test.pages import HomePage, AdminPage


class PageLoadingTests(Test):

    def test_home_page_loads(self):
        home = HomePage(self.driver).open().wait_for_loading()
        assert home.title == "People's Archive of Rural India"

    def test_admin_page_loads(self):
        admin = AdminPage(self.driver).open().wait_for_loading()
        assert admin.title.startswith("Log in")
