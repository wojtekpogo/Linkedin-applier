from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import re

class submitLinkedin:

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
        total_jobs_on_the_page = 24
        # Amount of jobs displayed on one page +1
        job_steps = 25

        total_offers = self.driver.find_element_by_class_name("display-flex.t-12.t-black--light.t-normal")
        total_results  = int(total_offers.text.split(' ',1)[0].replace(",",""))
        #print(total_results)
        time.sleep(1)
        current_page = self.driver.current_url
        results = self.driver.find_elements_by_class_name("jobs-search-results__list-item.occludable-update.p0.relative.ember-view")

        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            job_title = result.find_elements_by_class_name("disabled.ember-view.job-card-container__link.job-card-list__title")

            for title in job_title:
                self.submit(title)
        
        if total_results > total_jobs_on_the_page:
            time.sleep(1)

            # Find the last page
            find_page = self.driver.find_element_by_class_name("artdeco-pagination__indicator.artdeco-pagination__indicator--number")
            total_page = find_page[len(find_page-1)].text
            total_page_int = int(re.sub(r"[^\d.","",total_page))
            get_last_page = self.driver.find_element_by_xpath("//button[@aria-label='Page "+str(total_page_int)+"']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url
            total_jobs = int(last_page.split('start=',1)[1])

            # Loop through all available job options

            for page_number in range(job_steps,total_jobs+job_steps,job_steps):
                self.driver.get(current_page+"&start="+str(page_number))
                time.sleep(2)
                results_e = self.driver.find_element_by_class_name("jobs-search-results__list-item.occludable-update.p0.relative.ember-view")

                for result_e in results_e:
                    hover = ActionChains(self.driver).move_to_element(result_e)
                    hover.perform()
                    job_title_e = result_e.find_element_by_class_name("disabled.ember-view.job-card-container__link.job-card-list__title")

                    for title_e in job_title_e:
                        self.submit(title_e)
        else:
            self.close()

    

    def close(self):
        """Closes the application"""

        print("Session ended.")
        self.driver.close()

   
    def submit(self,job):
        """This function submit the application for the selected job"""

         # 1. only apply for the jobs that doesnt redirect to the different page

        print("You applied to ",job.text)
        job.click()
        time.sleep(2)

         # Click on the easy apply

        current_url = self.driver.current_url

        try:
            submit_click = self.driver.find_element_by_class_name("jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view").click()
        except NoSuchElementException:
            print("Already applied.")
            pass

            
        # Try to submit application
        try:
            # Next button
            submit = self.driver.find_element_by_class_name("jobs-submit-button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view").click()

            # Review Button
            review_button = WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.CLASS_NAME,
            "jobs-submit-button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view"))).click()

            # Uncheck the checkbox
            check_box = self.driver.find_element_by_xpath("//input[starts-with(@id,'follow-company-checkbox')]")
            
            

        except NoSuchElementException:
            print("Unable to submit")
            try:
                discard = self.driver.find_element_by_xpath("//button[@data-test-modal-close-btn]").click()
                time.sleep(1)
                confirm_discard = self.driver.find_element_by_xpath("//button[@data-test-dialog-btn").click()
            except NoSuchElementException:
                pass

    def apply(self):

        self.driver.maximize_window()
        # Login
        self.login()
        time.sleep(2)
        # Job Search
        self.job_search()
        time.sleep(3)
        # Filter job offers
        self.filter()
        time.sleep(2)
        self.find_job()
        time.sleep(2)
        self.close()
                    
if __name__ == "__main__":

    with open('config.json') as config:
        data = json.load(config)
    bot = submitLinkedin(data)
    bot.apply()
  
