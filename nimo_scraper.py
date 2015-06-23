# # TO DO
#     - convert start_date to actual dattime object
#     - update path with wiedld or user info, imported from os environ
#     - update date in xml file path
#     - click on window for xml download
#         - try/except on this window


from selenium import webdriver
import selenium.webdriver.firefox.webdriver
import selenium.webdriver.common.alert
# The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import csv
import re
import xml.etree.ElementTree as ET


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
        """login to nimo acct. (National Grid, Niagara Mohawk)"""

        login_id = self.browser.find_element_by_id("MainContent_UCSignIn_txtSigninID")
        login_id.send_keys(self.user_login)

        pwd = self.browser.find_element_by_id("MainContent_UCSignIn_txtPassword")
        pwd.send_keys(self.user_pwd)

        self.browser.find_element_by_id("MainContent_UCSignIn_btnSignin").click()

        time.sleep(0.2)         # let login process complete

        # confirm login successful
        try:
            assert "National Grid - StateLandingNY" in self.browser.title
        except:
            print "login failed"


    def convert_xml_to_csv(self, path):
        """take downloaded nimo data in xml, and export to csv. xml schema standard is here: https://naesb.org//copyright/espi.xsd"""

        xml_stream = self.xml_stream_generator(path)

        new_filename = "%s_usage_cost.csv" % self.user_login
        with open(new_filename, "w") as fp:
            row_for_timept = csv.writer(fp, delimiter=",")

            for line in xml_stream:
                datapoint = ET.fromstring(line)

                for child in datapoint.iter():
                    if child.tag == '{http://naesb.org/espi}start':
                        start_date = child.text
                    if child.tag == '{http://naesb.org/espi}value':
                        value = child.text
                    if child.tag == '{http://naesb.org/espi}cost':
                        cost = float(child.text)/(10**4)  # 4 decimal places

                row_for_timept.writerow([start_date, value, cost])


    def xml_stream_generator(self, path):
        """generate streaming xml from file. yields xml data blocks."""

        node_start = lambda x: re.match("<ns:IntervalBlock", x) != None
        node_end = lambda x: re.match("</ns:IntervalBlock", x) != None

        with open(path) as f:
            node = ""
            for line in f:
                l = line.strip()
                if node_start(l):
                    node = ""
                node = node + l
                if node_end(l):
                    yield node


    def get_usage_data(self):
        self.setup()

        self.browser.get("https://www1.nationalgridus.com/SignIn-NY-RES")
        assert "My National Grid profile sign-in" in self.browser.title

        self.login_nimo()

        self.browser.find_element_by_id("MainContent_StateLandingNY1_Hyperlink44").click()

        self.browser.find_element_by_id("MainContent_TabContainerUsageAndCost_TabPanelElectricityUsage_ElectricityUsageView_UCElectricityUsage_hlkXML").click()
        ######################################################

        # dwnload_alert = self.browser.switch_to_frame("Opening ElectricityXMLdata6_22_2015")
        time.sleep(0.2)
        dwnload_alert = self.browser.switch_to_alert()
        time.sleep(0.2)
        # alert_driver = dwnload_alert.driver
        # alert_driver.send_keys(Keys.RETURN)
        # print dwnload_alert

        # alert_driver = dwnload_alert.driver
        # sub_button = alert_driver.find_element_by_tag_name('input')
        # print sub_button

        # ele = dwnload_alert.getAlertText
        # print ele

        ###################################
        # download will be named with date in format "ElectricityXMLdata6_22_2015"
        # ###################################
        # path = "/Users/wiedld/Downloads/ElectricityXMLdata6_23_2015"
        # self.convert_xml_to_csv(path)

        # self.tear_down()
        print "Task complete for %s" % (self.user_login)


if __name__ == "__main__":
    testcase = UtilityAccount("nimo", test_login, test_pwd)
    # testcase.get_usage_data()
    path = "/Users/wiedld/Downloads/ElectricityXMLdata6_23_2015"
    testcase.convert_xml_to_csv(path)
