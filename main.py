import os
# import json
from csv import writer, reader
# import pandas as pd
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


# Returns companies url from the csv file for parsing
def url_grabber(company_name):
    with open('companies.csv', newline='') as csv_file:
        csv_reader = reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == company_name:
                company_url = " ".join(row).split(" ")[1]
                break
            else:
                company_url = "Not found"
        return company_url



# Pulls a sits html data to test parsing
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

# Adds a new company/url to the csv file
def company_writer(company):
    with open('companies.csv', 'a', newline='') as f:
        f.write('\n')
        writer_obj = writer(f)
        writer_obj.writerow(company)



job_url = url_grabber("Mirador")
write_site(job_url)

# new_company = ["Anyptys Bio", "https://recruiting.paylocity.com/Recruiting/Jobs/All/d1d20c2d-0e1d-4869-820d-a5b454cfba0b/ANAPTYSBIO-INC"]
# company_writer(new_company)

