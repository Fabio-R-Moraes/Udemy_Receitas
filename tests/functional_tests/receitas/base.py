import time
from utils.browser import make_chrome_browser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from receitasApp.tests.test_receitas_base import ReceitaMixing

class ReceitaBaseFunctionalTest(StaticLiveServerTestCase, ReceitaMixing):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)