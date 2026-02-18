from src.site_scraper import sel_driver
from src.db_manager import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

site_url = get_company_url("Novartis")
site_driver = sel_driver(site_url)
# city_location = "San Diego, CA"

# Finds the location search button and input the city
try:
    checkbox = site_driver.find_element(By.CSS_SELECTOR, 'input[value="LOC_US"]')
except NoSuchElementException:
    print("Search button Not found")
else:
    site_driver.execute_script("arguments[0].click();", checkbox)
    submit = site_driver.find_element(By.ID, 'edit-submit')
    submit.click()

try:
    # Wait up to 10 seconds for the specific link to become clickable
    site_sort_link = WebDriverWait(site_driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="sort by Site"]'))
    )
    print("Site header link found!")
    site_sort_link.click()
    print("Successfully clicked the Site header.")

except TimeoutException:
    print("Site header link not found or did not become clickable.")


# site_button = WebDriverWait(site_driver, 3).until(
#     ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="sort by Site"]')))
# site_button.click()

# Finds the element with the job and waits until it's available.
# try:
#     job_element = WebDriverWait(site_driver, 10).until(
#         ec.visibility_of_element_located((By.CSS_SELECTOR, ".job-title")))
# except NoSuchElementException:
#     print("element not found")
# else:
#     job_titles = site_driver.find_elements(By.CSS_SELECTOR, ".job-title")
#     job_locations = site_driver.find_elements(By.CSS_SELECTOR, ".job-location")
#     job_url = site_driver.find_elements(By.CSS_SELECTOR, 'a[data-ph-at-id="job-link"]')
#
#     for job in range(len(job_titles)):
#         title = job_titles[job].text.strip()
#         clean_location = job_locations[job].text.replace("Location", "").strip().split(",")
#         location = ",".join(clean_location[:2])
#         url = job_url[job].get_attribute("href")
#         if title:
#             add_job("Lilly", title, location, url)
# site_driver.quit()
