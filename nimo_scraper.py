
"""


"""

#################################################################

from selenium import webdriver
import selenium.webdriver.firefox.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime, date
import os, os.path
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
        """start selenium web server. set download settings for xml file."""

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", "/tmp/")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.xml")

        self.browser = webdriver.Firefox(firefox_profile=profile)
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
        """navigating throught the utility website, downloading the xml file, and converting to csv saved to . directory."""

        self.setup()

        self.browser.get("https://www1.nationalgridus.com/SignIn-NY-RES")
        assert "My National Grid profile sign-in" in self.browser.title

        self.login_nimo()

        self.browser.find_element_by_id("MainContent_StateLandingNY1_Hyperlink44").click()

        self.browser.find_element_by_id("MainContent_TabContainerUsageAndCost_TabPanelElectricityUsage_ElectricityUsageView_UCElectricityUsage_hlkXML").click()

        # determine path of downloaded file
        url_date = (date.today()).strftime('%m_%d_%Y')
        # url doesn't have zero-padded month
        url_date = url_date.lstrip('0')
        path = "/tmp/ElectricityXMLdata%s" % url_date
        self.convert_xml_to_csv(path)

        self.tear_down()
        print "Task complete for %s" % (self.user_login)


if __name__ == "__main__":
    testcase = UtilityAccount("nimo", test_login, test_pwd)
    testcase.get_usage_data()

