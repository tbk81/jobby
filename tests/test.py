# from src.site_scraper import sel_driver
# from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSelectorException
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
#
url = "https://careers.abbvie.com/en/jobs?q=San_Diego&options=&page=1"
#
# site_driver = sel_driver(url)
#
# try:
#     # Finds the element with the job and waits until it's available.
#     WebDriverWait(site_driver, 10).until(
#         ec.visibility_of_element_located((By.CLASS_NAME, "attrax-vacancy-tile")))
# # except NoSuchElementException as error:
# #     print(f"element not found: {error}")
# # except TimeoutException as error:
# #     print(f"timeout: {error}")
# # except InvalidSelectorException as error:
# #     print(f"invalid selector: {error}")
# except Exception as e:
#     print(e)
#     site_driver.quit()
# else:
#     job_titles = site_driver.find_elements(By.CLASS_NAME, 'attrax-vacancy-tile__title')
#     # print(f"Successfully found {len(job_titles)} job titles!\n")
#     try:
#         jobs = site_driver.find_elements(By.CLASS_NAME, 'attrax-vacancy-tile__title')
#     except Exception as e:
#         print(e)
#         site_driver.quit()
#     else:
#         for job in jobs:
#             print(job.text)
#             print(job.get_attribute('href'))
#         # print(title_test[0].text)
#     # job_locations = site_driver.find_elements(By.CSS_SELECTOR, "div:nth-child(2)")
#     # job_url = site_driver.find_elements(By.CSS_SELECTOR, ".title")
#     site_driver.quit()
#
#
#
#
#
#     # for job in range(len(job_titles)):
#     #     print(job_titles[job].text.strip())
#     #     print(job_titles[job].get_attribute("href"))
#         # print(job_locations[job].text)
#     #     title = job_titles[job].text.strip()
#     #     location = job_locations[job].text.replace("\n", "")
#     #     job_url = job_titles[job].get_attribute("href")
#     #     if "Diego" in location:
#     #         pass
# site_driver.quit()

import requests
from bs4 import BeautifulSoup


def scrape_jobs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []

    # Find every <a> tag that has the 'attrax-vacancy-tile__title' class
    for job_link in soup.find_all('a', class_='attrax-vacancy-tile__title'):
        jobs.append({
            "title": job_link.text.strip(),
            "url": "https://careers.abbvie.com" + job_link.get('href') if job_link.get('href').startswith(
                '/') else job_link.get('href'),
            "location": "San Diego, CA",
            "company": "AbbVie"
        })

    return jobs

abbvie = scrape_jobs(url)
print(abbvie)
