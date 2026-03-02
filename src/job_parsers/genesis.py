from src.site_scraper import sel_driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def scrape_jobs(url):
    print(url)
    site_driver = sel_driver(url)
    scraped_data = []

    try:
        # Finds the element with the job and waits until it's available.
        WebDriverWait(site_driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".title")))
    except NoSuchElementException:
        print("element not found")
    else:
        job_titles = site_driver.find_elements(By.CSS_SELECTOR, ".title")
        job_locations = site_driver.find_elements(By.CSS_SELECTOR, ".locations-container")
        # job_url = site_driver.find_elements(By.CSS_SELECTOR, ".title")

        for job in range(len(job_titles)):
            title = job_titles[job].text.strip()
            location = job_locations[job].text.replace("\n", "")
            job_url = job_titles[job].get_attribute("href")
            if "Diego" in location:
                scraped_data.append({
                    "title": title,
                    "location": location,
                    "url": job_url
                })
    site_driver.quit()

    return scraped_data
