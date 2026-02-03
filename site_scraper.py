import os
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

headers = {
    "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",

    }

# Chrome and driver setup for selenium
def sel_driver(url, name):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')

    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(5)
    with open(f'html_data/{name}.html', 'w') as file:
        file.write(driver.page_source)
    driver.close()

# Pulls site HTML data to test parsing; this does not work for dynamic sites
def write_site(url, name):
    job_response = requests.get(url, headers=headers)
    with open(f'html_data/{name}.html', 'w') as file:
        file.write(job_response.text)


url = 'https://www.miradortx.com/careers?gh_tag=all_jobs#all_jobs'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument('--headless')

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
driver.implicitly_wait(3)
try:
    button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
except NoSuchElementException:
    print("Accept cookies button not found")
else:
    button.click()
try:
    # html = driver.find_element(By.CSS_SELECTOR, "p.body.body--medium")
    frame = driver.find_element(By.CLASS_NAME, "job-posts--table")
    driver.switch_to.frame(frame)
    # html = driver.find_elements(By.CLASS_NAME, "p")
    # html = driver.find_elements(By.TAG_NAME, "tr")
    # html = driver.find_element(By.CSS_SELECTOR, "div.job-posts")
    # html = driver.find_element(By.CSS_SELECTOR, "p.body.body--medium")
    # html = driver.find_elements(By.XPATH, "//p[@class='body body--medium']")
    html = driver.find_element(By.XPATH, "//p[contains(@class, 'body--medium')]")
    # html = driver.find_element(By.XPATH, "/html/body/main/div/div[2]/div[2]/div/div[1]/div/table/tbody/tr/td/a/p[1]")
    # innerHTML = driver.execute_script("return document.body.innerHTML")
except NoSuchElementException:
    print("element not found")
else:
    print(html)
# for p in html:
#     print(p.text)

# job_titles = driver.find_element(By.CSS_SELECTOR, 'p.body.body--medium')
# driver.quit()
# print(job_titles)
