from src.site_scraper import sel_driver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSelectorException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

url = "https://treeline.bio/careers"

site_driver = sel_driver(url)
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
    print(f"Successfully found {len(job_cards)} job cards! Starting extraction...\n")
    # job_locations = site_driver.find_elements(By.CSS_SELECTOR, "div:nth-child(2)")
    # job_url = site_driver.find_elements(By.CSS_SELECTOR, ".title")
    detail_blocks = site_driver.find_elements(By.XPATH, "//div[contains(@class, 'flex-1')]")

    for block in detail_blocks:

        # Grab the title elements
        titles = block.find_elements(By.XPATH, "./div[1]")
        if not titles:
            continue

        # Extract the text
        job_title = titles[0].text.strip()

        # --- NEW ADDITION ---
        # If the text we grabbed is completely empty, it's a ghost block and skip it
        if job_title == "":
            continue
        # -------------------

        # Grab Location
        locations = block.find_elements(By.XPATH, ".//div[contains(@class, 'text-[15px]')]")
        job_location = locations[0].text.strip() if locations else "No Location"

        # Grab Date
        dates = block.find_elements(By.XPATH, ".//div[contains(@class, 'text-[13px]')]")
        job_date = dates[0].text.strip() if dates else "No Date"

        # Grab URL
        links = block.find_elements(By.XPATH, "./following-sibling::div//a")
        job_url = links[0].get_attribute('href') if links else "No Link"

        print(f"Title:    {job_title}")
        print(f"Location: {job_location}")
        print(f"Updated:  {job_date}")
        print(f"Link:     {job_url}")
        print("-" * 50)

    # for job in range(len(job_titles)):
        # print(job_titles[job].text.strip())
        # print(job_locations[job].text)
    #     title = job_titles[job].text.strip()
    #     location = job_locations[job].text.replace("\n", "")
    #     job_url = job_titles[job].get_attribute("href")
    #     if "Diego" in location:
    #         pass
site_driver.quit()