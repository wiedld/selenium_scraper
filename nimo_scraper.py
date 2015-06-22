from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
from selenium.webdriver.common.keys import Keys
import time


class NimoAccount(object):

    def __init__(self, user_login, user_pwd):
        self.user_login = user_login
        self.user_pwd = user_pwd


    def load_website(self):
        """start selenium web server and load nimo website"""
        self.browser = webdriver.Firefox()
        self.browser.get("https://www1.nationalgridus.com/SignIn-NY-RES")
        assert "My National Grid profile sign-in" in self.browser.title

        self.login_id = self.browser.find_element_by_id("MainContent_UCSignIn_txtSigninID")
        self.pwd = self.browser.find_element_by_id("MainContent_UCSignIn_txtPassword")

        print "NiMO website loaded for %s" % (self.user_login)


    def tear_down(self):
        self.browser.close()
        print "teardown complete for %s" % (self.user_login)


# # next page loads
# time.sleep(0.2)


if __name__ == "__main__":
    testcase = NimoAccount("login","pwd")
    testcase.load_website()
    testcase.tear_down()

