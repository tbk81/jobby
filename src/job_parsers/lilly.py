from src.site_scraper import sel_driver
from src.db_manager import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

site_url = get_company_url("Lilly")
site_driver = sel_driver(site_url)
city_location = "San Diego, CA"


def scrape_jobs(url):
    scraped_data = []
    # Finds the location search button and input the city
    try:
        button = site_driver.find_element(By.ID, "gllocationInput")
    except NoSuchElementException:
        print("Search button Not found")
    else:
        button.send_keys(city_location)
        button.send_keys(Keys.RETURN)

    # Finds the element with the job and waits until it's available.
    try:
        WebDriverWait(site_driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".job-title")))
    except NoSuchElementException:
        print("element not found")
    else:
        job_titles = site_driver.find_elements(By.CSS_SELECTOR, ".job-title")
        job_locations = site_driver.find_elements(By.CSS_SELECTOR, ".job-location")
        job_url = site_driver.find_elements(By.CSS_SELECTOR, 'a[data-ph-at-id="job-link"]')

        for job in range(len(job_titles)):
            title = job_titles[job].text.strip()
            clean_location = job_locations[job].text.replace("Location", "").strip().split(",")
            location = ",".join(clean_location[:2])
            url = job_url[job].get_attribute("href")
            # if title:
            #     add_job("Lilly", title, location, url)
            scraped_data.append({
                "title": title,
                "location": location,
                "url": url
            })
    site_driver.quit()

    return scraped_data
