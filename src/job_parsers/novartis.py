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

# Finds the sort by location link and presses it twice
site_sort_locator = (By.CSS_SELECTOR, 'a[title="sort by Site"]')
try:
    # Wait ONLY for the element to exist in the HTML, not for it to be "clickable"
    first_sort_link = WebDriverWait(site_driver, 10).until(
        ec.presence_of_element_located(site_sort_locator))
    # Force the click using JavaScript to bypass any overlapping elements
    site_driver.execute_script("arguments[0].click();", first_sort_link)

    # Click the element again for descending
    WebDriverWait(site_driver, 10).until(
        ec.staleness_of(first_sort_link))
    second_sort_link = WebDriverWait(site_driver, 10).until(
        ec.presence_of_element_located(site_sort_locator))
    site_driver.execute_script("arguments[0].click();", second_sort_link)



except TimeoutException:
    print("Link completely missing. It might be inside an iframe or the page hasn't loaded.")


# xpath_selector = "//th[contains(@class, 'views-field-field-job-work-location')]/a"
# site_sort_link = site_driver.find_element(By.XPATH, xpath_selector)
# site_sort_link.click()

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
