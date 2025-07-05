from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def extract_reviews(row):
	output_dict = {
		'rating': [],
		'review_text': [],
		'course_name': [],
		'provider': []
	}
	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service)

	driver.get(row['course_link'])
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
			if count > 15:
				break
		except:
			break
	
	print("Sleeping for a bit")
	time.sleep(3)

	course_review_section = driver.find_element(By.ID, "providerCourseReviews")
	review_content = course_review_section.find_elements(By.CLASS_NAME, "review-content")
	provider = driver.find_element(By.CLASS_NAME, "provider-link")
	for i in review_content:
		rating = i.find_element(By.CLASS_NAME, "rating").get_attribute("alt")
		try:
			review_list = []
			review_text = i.find_elements(By.TAG_NAME, "p")
			for j in review_text:
				review_list.append(j.get_attribute("innerHTML"))
		except Exception as e:
			print(f'Encountered the following error:{e}')
			review_text = ""
		output_dict['rating'].append(rating)
		output_dict['review_text'].append(review_list)
		output_dict['course_name'].append(row['course_title'])
		output_dict['provider'].append(provider.text)

	time.sleep(4)
	return pd.DataFrame(output_dict)

data = pd.read_csv('id_extracted_links.csv')

output = pd.DataFrame({
    'rating': [],
    'review_text': [],
	'course_name': [],
	'provider': []
})
top_ten = 10
for index, row in data.iterrows():
	output = pd.concat([extract_reviews(row), output], ignore_index=True)
	top_ten -= 1
	if top_ten <= 0:
		break

output.to_csv('temp.csv')