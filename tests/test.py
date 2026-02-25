from src.site_scraper import sel_driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

URL = "https://genesis.ml/careers/"

site_driver = sel_driver(URL)

# Finds the element with the job and waits until it's available.
try:
    WebDriverWait(site_driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, ".title")))
except NoSuchElementException:
    print("element not found")
else:
    job_titles = site_driver.find_elements(By.CSS_SELECTOR, ".title")
    job_locations = site_driver.find_elements(By.CSS_SELECTOR, ".location")
    # job_url = site_driver.find_elements(By.ID, 'a[id="hiringthing-jobs"]')

    for job in range(len(job_titles)):
        print(job_titles[job].text.strip())
        print(job_locations[job].text.replace("/", "").strip())
        # print(job_titles[job].get_attribute("href"))
        # if title:
        #     add_job("Lilly", title, location, url)
        # scraped_data.append({
        #     "title": title,
        #     "location": location,
        #     "url": url
        # })
site_driver.quit()



