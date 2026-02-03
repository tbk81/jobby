from site_scraper import sel_driver
from company_manager import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

site_driver = sel_driver(url_grabber("Mirador"))

try:
    button = site_driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
except NoSuchElementException:
    print("Accept cookies button not found")
else:
    button.click()

try:
    frame = site_driver.find_element(By.ID, "grnhse_iframe")
    site_driver.switch_to.frame(frame)
    # driver.
    job_titles = site_driver.find_elements(By.XPATH, "//p[@class='body body--medium']")
    job_urls = site_driver.find_elements(By.TAG_NAME, "a")
except NoSuchElementException:
    print("element not found")
else:
    for i in range(len(job_titles)):
        print(job_titles[i].text)
        print(job_urls[i].text)
site_driver.quit()


# job_titles = driver.find_element(By.CSS_SELECTOR, 'p.body.body--medium')
# driver.quit()
# print(job_titles)



# with open('/Users/trevor/jobby/html_data/mirador.html') as file:
# with open('/home/trevor/python-projects/jobby/html_data/janux.html') as file:
#     mirador_data = file.read()
# soup = BeautifulSoup(mirador_data, 'html.parser')
#
# job_titles = soup.find_all('h5')
# job_locations = soup.find_all('span', class_='sort-by-location posting-category small-category-label location')
# job_urls = soup.find_all('a', class_='posting-btn-submit template-btn-submit cerulean')

# for i in range(len(job_titles)):
#     print(job_titles[i].text.strip())
#     print(job_locations[i].get_text(strip=True))
#     print(job_urls[i]['href'].strip())
#     print("\n")
