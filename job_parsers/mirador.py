from site_scraper import sel_driver
from company_manager import *
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
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
    html = site_driver.page_source
    # job_titles = site_driver.find_elements(By.XPATH, "//p[@class='body body--medium']")
    # job_urls = site_driver.find_elements(By.TAG_NAME, "a")
except NoSuchElementException:
    print("element not found")
else:
    with open(f'/Users/trevor/jobby/html_data/mirador.html', 'w') as file:
        file.write(html)
site_driver.quit()

with open('/Users/trevor/jobby/html_data/mirador.html') as file:
    # with open('/home/trevor/python-projects/jobby/html_data/mirador.html') as file:
    mirador_data = file.read()
soup = BeautifulSoup(mirador_data, 'html.parser')
#
job_titles = soup.find_all('p', class_='body body--medium')
job_locations = soup.find_all('p', class_='body body__secondary body--metadata')
job_urls = soup.find_all('a')

for i in range(len(job_titles))[1:]:
    print(job_titles[i].text)
    print(job_locations[i - 1].get_text(strip=True))
    print(job_urls[i - 1]['href'].strip("#all_jobs"))
    # print("\n")
