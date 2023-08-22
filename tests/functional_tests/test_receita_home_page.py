import time
#from django.test import LiveServerTestCase
from utils.browser import make_chrome_browser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

class ReceitaHomePageFunctionalTest(StaticLiveServerTestCase):
    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_the_test(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        self.sleep(6)
        temp = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Não há receitas para mostrar...', temp.text)
        browser.quit()

