from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class ApplyLinkedin:

    def __init__(self,data):
        """Parameters"""

        self.email = data['email']
        self.password = data['password']
        self.keyword = data['keyword']
        self.location = data['location']
        self.driver = webdriver.Chrome(data['driver_path'])

    def login(self):
        """Logs in to your profile"""

        self.driver.get("https://www.linkedin.com/")

        # email
        login_email = self.driver.find_element_by_name("session_key")
        login_email.clear()
        login_email.send_keys(self.email)
        
        login_password = self.driver.find_element_by_name("session_password")
        login_password.clear()
        login_password.send_keys(self.password)
        login_password.send_keys(Keys.RETURN)


    def job_search(self):
        # close messages window
        # close_messages = self.driver.find_element_by_xpath('//*[@id="ember175"]')
        # close_messages.click()
        # time.sleep(1)

        #jobs = self.driver.find_element_by_link_text('Jobs')
        jobs = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.LINK_TEXT,"Jobs"))).click()
        #jobs.click()
        time.sleep(2)


        # keywords
        search_job = self.driver.find_element_by_xpath("//input[starts-with(@id, 'jobs-search-box-keyword')]")
        search_job.clear()
        search_job.send_keys(self.keyword)

        # night night
        time.sleep(2)

        # location
        search_location = self.driver.find_element_by_xpath("//input[starts-with(@id, 'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
        time.sleep(2)

        # Locate the search button and click it
        search = self.driver.find_element_by_xpath("//button[text()='Search']")
        search.click()
        time.sleep(1)

    def filter(self):
        """This function applies 'easy apply' option"""
 
        self.driver.find_element_by_xpath('//button[contains(@aria-label, "Easy Apply filter.")]').click()
        time.sleep(1)
    
    def find_job(self):
        """This function filters through the jobs"""

        total_offers = self.driver.find_element_by_class_name("display-flex.t-12.t-black--light.t-normal")
        total_results  = int(total_offers.text.split(' ',1)[0].replace(",",""))
        #print(total_results)
        time.sleep(1)



        
if __name__ == "__main__":

    with open('config.json') as config:
        data = json.load(config)
    bot = ApplyLinkedin(data)
    bot.login()
    time.sleep(2)
    bot.job_search()
    time.sleep(2)
    bot.filter()
    time.sleep(2)
    bot.find_job()
