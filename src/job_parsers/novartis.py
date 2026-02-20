from src.site_scraper import sel_driver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def scrape_jobs(url):
    site_driver = sel_driver(url)
    scraped_data = []

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

    # Finds the element with the job and waits until it's available.
    job_locator = (By.CSS_SELECTOR, 'td[class="views-field views-field-field-job-title"]')
    try:
        job_titles = WebDriverWait(site_driver, 10).until(
            ec.visibility_of_all_elements_located(job_locator))
    except NoSuchElementException:
        print("element not found")
    else:
        for job in job_titles:
            try:
                # Title and URL (Your existing code)
                link_element = job.find_element(By.TAG_NAME, 'a')
                job_url = link_element.get_attribute('href')
                job_title = link_element.text.strip()

                # Location
                # The "../" tells Selenium to go up to the <tr>, then it finds the location <td>
                location_element = job.find_element(By.XPATH, "../td[contains(@class, 'field-job-work-location')]")
                job_location = location_element.text.strip()

            except NoSuchElementException:
                # Fallback if a row is missing data
                job_title = job.text.strip()
                job_url = "No link available"
                job_location = "Unknown"

            if job_location == "San Diego":
                scraped_data.append({
                    "title": job_title,
                    "location": job_location,
                    "url": job_url
                })

    site_driver.quit()

    return scraped_data
