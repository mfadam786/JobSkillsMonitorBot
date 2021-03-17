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
        self.driver.get('https://www.seek.co.nz/jobs-in-information-communication-technology/')

        # link = self.driver.find_element_by_xpath("//a[@data-automation='jobTitle']")
        # print(link.get_attribute('href'))

        # links = self.driver.find_element_by_xpath("//a[@data-automation='jobTitle']")
        # links = self.driver.find_element_by_xpath("href(//a[@data-automation='jobTitle'])")

        links = []
        for i in range(1,23):
            links.append(self.driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[2]/section/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[" + str(i) + "]/article/span[2]/span/h1/a"))

        for link in links:
            print(link.get_attribute('href'))
        self.driver.get('https://en.wikipedia.org/wiki/List_of_programming_languages')
        for i in self.driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[5]/div[1]/div[@class='div-col']/ul[*]/li"):
            print(i.getText())
        
        # length = 0
        # # length = len(self.driver.find_element_by_xpath("//a[@data-automation='jobTitle']"))

        # eof = False

        # while not(eof):
        #     try:
        #         link = self.driver.find_element_by_xpath("//a[@data-automation='jobTitle']")
        #         length += 1
        #         print(link.get_attribute('href'))
        #         print(length)
        #     except:
        #         eof = True

        # print('Showing result: ')
        # print(link.get_attribute('href') for link in links)
        # print('Done!')


        # elem_quiz_name = self.driver.find_element_by_id("id_name")
        # elem_quiz_name.send_keys('Test')

        # elem_category = self.driver.find_element_by_xpath("//select[@id='id_category']")
        # elem_category.send_keys(elem_category.selectVisibleText('General Knowledge'))

        # elem_difficulty = self.driver.find_element_by_xpath("//select[@id='id_difficulty']")
        # elem_difficulty.send_keys(elem_difficulty.selectVisibleText('Random'))

        # elem_start_date = self.driver.find_element_by_xpath("//select[@id='id_start_date']")
        # elem_start_date.send_keys('23102020')
        # elem_start_date.sendKeys(Keys.TAB)
        # elem_start_date.sendKeys("0245PM")

        # elem_end_date = self.driver.find_element_by_xpath("//select[@id='id_end_date']")
        # elem_end_date.send_keys('30102020')
        # elem_end_date.sendKeys(Keys.TAB)
        # elem_end_date.sendKeys("0245PM")

        # submit = self.driver.find_element_by_id('create_quiz').click()
        
        # self.assertTrue('You have successfully created a new quiz tournament' in self.driver.page_source)
