from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def extract_reviews(page):
	output_dict = {
		'rating': [],
		'review_text': []
	}
	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service)

	driver.get(page)
	time.sleep(5)

	accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
	accept_button.click()
	course_review_section = driver.find_element(By.ID, "providerCourseReviews")
	while True:
		try:
			links = course_review_section.find_elements(By.TAG_NAME, 'a')
			links[1].send_keys("", Keys.ENTER)
		except:
			break

	course_review_section = driver.find_element(By.ID, "providerCourseReviews")
	review_content = course_review_section.find_elements(By.CLASS_NAME, "review-content")
	for i in review_content:
		rating = i.find_element(By.CLASS_NAME, "rating").get_attribute("alt")
		try:
			review_text = i.find_element(By.CLASS_NAME, "mt-1").text.strip()
		except:
			review_text = ""
		output_dict['rating'].append(rating)
		output_dict['review_text'].append(review_text)

	pd.DataFrame(output_dict).to_csv("reviews.csv", index=False)

	time.sleep(4)

extract_reviews('https://www.reed.co.uk/courses/data-analytics-power-bi-tableau-python-cloud-computing-analyst-microsoft-excel-it/416128')