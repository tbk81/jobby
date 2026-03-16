from src.site_scraper import sel_driver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSelectorException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

url = "https://careers.abbvie.com/en/jobs?q=San_Diego&options=&page=1"

site_driver = sel_driver(url)

try:
    # Finds the element with the job and waits until it's available.
    WebDriverWait(site_driver, 10).until(
        ec.visibility_of_element_located((By.CLASS_NAME, "attrax-vacancy-tile")))
# except NoSuchElementException as error:
#     print(f"element not found: {error}")
# except TimeoutException as error:
#     print(f"timeout: {error}")
# except InvalidSelectorException as error:
#     print(f"invalid selector: {error}")
except Exception as e:
    print(e)
    site_driver.quit()
else:
    job_titles = site_driver.find_elements(By.CSS_SELECTOR, ".attrax-vacancy-tile__title")
    # print(f"Successfully found {len(job_titles)} job titles!\n")
    try:
        title_test = site_driver.find_elements(By.CSS_SELECTOR, "[.attrax-vacancy-tile__title] tabindex")
    except Exception as e:
        print(e)
        site_driver.quit()
    else:
        print(title_test)
    # job_locations = site_driver.find_elements(By.CSS_SELECTOR, "div:nth-child(2)")
    # job_url = site_driver.find_elements(By.CSS_SELECTOR, ".title")
    site_driver.quit()





    # for job in range(len(job_titles)):
    #     print(job_titles[job].text.strip())
    #     print(job_titles[job].get_attribute("href"))
        # print(job_locations[job].text)
    #     title = job_titles[job].text.strip()
    #     location = job_locations[job].text.replace("\n", "")
    #     job_url = job_titles[job].get_attribute("href")
    #     if "Diego" in location:
    #         pass
site_driver.quit()