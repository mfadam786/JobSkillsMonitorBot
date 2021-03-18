from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from requests import get
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class TestGetLinks(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome('backend/chromedriver.exe')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    # Tests if an admin can create a quiz
    def test_create_quiz(self):


        # self.driver.get('https://www.seek.co.nz/jobs-in-information-communication-technology/')


        # for link in self.driver.find_elements_by_xpath("//a[@data-automation='jobTitle']"):
        #     print(link.get_attribute('href'))

        
        #------------------------------------------

        # self.driver.get('https://en.wikipedia.org/wiki/List_of_programming_languages')
               
        # languages = []
        # languages = self.driver.find_elements_by_xpath("//*[@id='mw-content-text']/div[1]/div[@class='div-col']/ul[*]/li")

        # f = open("List_Programming_Languages.txt", "w", encoding='utf-8')
        # for lang in languages:
        #     f.write(lang.text + '\n')
        #     print(lang.text)

        # f.close()

        #--------------------------------------------------------------------------------------------

        self.driver.get('https://en.wikipedia.org/wiki/Comparison_of_web_frameworks')

        # print(dir(self.driver))

        # fr = open("Frameworks.txt", "w", encoding='utf-8')

        for table in self.driver.find_elements_by_class_name("wikitable"):
            # fr.write(framework.text + '\n')
            print(table.find_elements_by_xpath("//td"))

            for row in table.find_elements_by_css_selector("tr"):
                print(row)
    
        # fr.close()