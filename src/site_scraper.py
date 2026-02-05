import os
import requests
from selenium import webdriver

headers = {
    "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",

    }

# Chrome and driver setup for selenium
def sel_driver(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')

    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)
    return driver

# Pulls site HTML data to test parsing; this does not work for dynamic sites
def write_site(url, name):
    job_response = requests.get(url, headers=headers)
    with open(f'html_data/{name}.html', 'w') as file:
        file.write(job_response.text)
