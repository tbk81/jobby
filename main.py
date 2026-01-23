import os
# import json
from csv import writer
# import pandas as pd
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By



# Chrome and driver setup
def chrome_driver(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)



def write_site(site):
    job_response = requests.get(site)
    with open('html_data/website.html', 'w') as file:
        file.write(job_response.text)



def title_parser():
    with open('html_data/website.html') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'html.parser')
    job_titles = soup.find_all('div')  #, class_='job-listing-container')
    print(job_titles)

# write_site(job_url)

def company_writer(company):
    with open('companies.csv', 'a', newline='') as f:
        f.write('\n')
        writer_obj = writer(f)
        writer_obj.writerow(company)



new_company = ["Anyptys Bio", "https://recruiting.paylocity.com/Recruiting/Jobs/All/d1d20c2d-0e1d-4869-820d-a5b454cfba0b/ANAPTYSBIO-INC"]
company_writer(new_company)

