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

	try:
		accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
		accept_button.click()
	except:
		pass
	course_review_section = driver.find_element(By.ID, "providerCourseReviews")
	count = 0
	while True:
		try:
			links = course_review_section.find_elements(By.TAG_NAME, 'a')
			links[1].send_keys("", Keys.ENTER)
			count += 1
			if count > 5:
				break
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

	time.sleep(4)
	return pd.DataFrame(output_dict)

data = pd.read_csv('id_extracted_links.csv')

output = pd.DataFrame({
    'rating': [],
    'review_text': []
})
top_ten = 10
for i in data['course_link']:
    output = pd.concat([extract_reviews(i), output], ignore_index=True)
    top_ten -= 1
    if top_ten == 0:
        break

output.to_csv('sample_output.csv')