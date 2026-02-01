from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from pathlib import Path

current_dir = Path.cwd()
root_dir = current_dir.parents[0]
data_dir = Path.joinpath(root_dir, "data")

base_url = "https://www.reed.co.uk/courses/discount"
reed_url = "https://www.reed.co.uk"

# We will collect the first 100 pages of courses and links. We will have a total of 2500 courses to work with.
def reed_courses_list():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(base_url)
    time.sleep(5)

    try:
        accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        accept_button.click()
    except:
        pass

    data = {
        'course_id': [],
        'course_name': [],
        'course_link': []
    }

    for index in range(1,101):
        print(f'Scraping page no: {index}')
        courses = driver.find_elements(By.CLASS_NAME, "course-card")

        for course in courses:
            course_id = course.get_attribute("id")
            course_title = course.find_element(By.CLASS_NAME, "course-card-title")
            course_name = course_title.text.strip()
            course_link = reed_url + course_title.find_element(By.TAG_NAME, "a").get_attribute("href")

            data["course_id"].append(course_id)
            data["course_name"].append(course_name)
            data["course_link"].append(course_link)

        pagination_item = driver.find_element(By.CLASS_NAME, "pagination")
        page_links = pagination_item.find_elements(By.TAG_NAME, "li")
        next_link = page_links[-1].find_element(By.TAG_NAME, "a")
        next_link.send_keys("" + Keys.ENTER)
        time.sleep(2)

    pd.DataFrame(data).to_csv(f'{data_dir}/reed_courses_with_links.csv', index=False)

def main():
    print("Collect the pages and links")
    reed_courses_list()

if __name__ == "__main__":
    main()