from src.site_scraper import sel_driver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSelectorException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

url = "https://treeline.bio/careers"

def scrape_jobs(url):
    site_driver = sel_driver(url)
    scraped_data = []

    title_xpath = "//div[contains(@class, 'text-[22px]') and contains(@class, 'font-serif')]"
    try:
        # Finds the element with the job and waits until it's available.
        WebDriverWait(site_driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, title_xpath)))
    except NoSuchElementException as error:
        print(f"element not found: {error}")
    except TimeoutException as error:
        print(f"timeout: {error}")
    except InvalidSelectorException as error:
        print(f"invalid selector: {error}")
    else:
        job_cards = site_driver.find_elements(By.XPATH, title_xpath)
        print(f"Successfully found {len(job_cards)} job cards. Starting extraction...\n")
        detail_blocks = site_driver.find_elements(By.XPATH, "//div[contains(@class, 'flex-1')]")

        for block in detail_blocks:

            # Grab the title elements
            titles = block.find_elements(By.XPATH, "./div[1]")
            if not titles:
                continue

            # Title
            job_title = titles[0].text.strip()

            # If the text grabbed is empty,skip it
            if job_title == "":
                continue
            # -------------------

            # Locations
            locations = block.find_elements(By.XPATH, ".//div[contains(@class, 'text-[15px]')]")
            job_location = locations[0].text.strip() if locations else "No Location"

            # URLs
            links = block.find_elements(By.XPATH, "./following-sibling::div//a")
            job_url = links[0].get_attribute('href') if links else "No Link"

            scraped_data.append({
                "title": job_title,
                "location": job_location,
                "url": job_url
            })

    site_driver.quit()

    return scraped_data