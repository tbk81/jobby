import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


# Chrome and driver setup for selenium
def chrome_driver(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

# Pulls site HTML data to test parsing; this does not work for dynamic sites
def write_site(site):
    job_response = requests.get(site)
    with open('html_data/website.html', 'w') as file:
        file.write(job_response.text)


# for testing how to parse the job titles and descriptions
def title_parser():
    with open('html_data/website.html') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'html.parser')
    job_titles = soup.find_all('div')  #, class_='job-listing-container')
    print(job_titles)