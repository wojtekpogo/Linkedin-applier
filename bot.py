from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
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

        jobs = self.driver.find_element_by_link_text('Jobs')
        jobs.click()


        # keywords
        search_job = self.driver.find_element_by_xpath("//input[starts-with(@id='jobs-search-box-keyword)]")
        search_job.clear()
        search.send_keys(self.keyword)

        # night night
        time.sleep(2)

        # location
        search_location = self.driver.find_element_by_xpath("//input[starts-with([@id='jobs-search-box-location')]")
        search_location.clear()
        search.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)












if __name__ == "__main__":

    with open('config.json') as config:
        data = json.load(config)
    bot = ApplyLinkedin(data)
    bot.login()
    time.sleep(3)
    bot.job_search()
