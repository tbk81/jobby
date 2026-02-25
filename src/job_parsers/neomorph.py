from src.site_scraper import sel_driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def scrape_jobs(url):
    site_driver = sel_driver(url)
    scraped_data = []
    try:
        WebDriverWait(site_driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".ht-title-link")))
    except NoSuchElementException:
        print("element not found")
    else:
        job_titles = site_driver.find_elements(By.CSS_SELECTOR, ".ht-title-link")
        job_locations = site_driver.find_elements(By.CSS_SELECTOR, ".ht-location")

        for job in range(len(job_titles)):
            title = job_titles[job].text.strip()
            location = job_locations[job].text.strip()
            job_url = job_titles[job].get_attribute("href")

            scraped_data.append({
                "title": title,
                "location": location,
                "url": job_url
            })

    return scraped_data
