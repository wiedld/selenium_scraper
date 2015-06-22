from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
from selenium.webdriver.common.keys import Keys
import time
import os


test_login = os.environ["nimo_test_login"]
test_pwd = os.environ["nimo_test_pwd"]


class UtilityAccount(object):

    def __init__(self, utility, user_login, user_pwd):
        self.utility = utility
        self.user_login = user_login
        self.user_pwd = user_pwd


    def setup(self):
        """start selenium web server"""
        self.browser = webdriver.Firefox()
        print "setup complete for %s" % (self.user_login)


    def tear_down(self):
        """start selenium web server"""
        self.browser.close()
        print "teardown complete for %s" % (self.user_login)


    def login_nimo(self):
        """login for nimo acct"""
        login_id = self.browser.find_element_by_id("MainContent_UCSignIn_txtSigninID")
        login_id.send_keys(self.user_login)

        pwd = self.browser.find_element_by_id("MainContent_UCSignIn_txtPassword")
        pwd.send_keys(self.user_pwd)

        self.browser.find_element_by_id("MainContent_UCSignIn_btnSignin").click()


    def get_usage_data(self):
        self.setup()

        self.browser.get("https://www1.nationalgridus.com/SignIn-NY-RES")
        assert "My National Grid profile sign-in" in self.browser.title

        self.login_nimo()

        # next page loads
        time.sleep(0.2)

        # self.tear_down()
        print "Task complete for %s" % (self.user_login)


if __name__ == "__main__":
    testcase = UtilityAccount("nimo",test_login,test_pwd)
    testcase.get_usage_data()

