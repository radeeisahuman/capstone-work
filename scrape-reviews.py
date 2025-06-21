from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get('https://www.reed.co.uk/courses/level-3-diploma-in-health-and-social-care--care-certificate-standards-1-to-15-course/348218')
time.sleep(10)

accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
accept_button.click()
course_review_section = driver.find_element(By.ID, "providerCourseReviews")
while True:
	try:
		links = course_review_section.find_elements(By.TAG_NAME, 'a')
		links[1].send_keys("", Keys.ENTER)
	except:
		break
time.sleep(4)