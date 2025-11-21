import requests
from bs4 import BeautifulSoup

job_url = "https://recruiting.paylocity.com/Recruiting/Jobs/All/d1d20c2d-0e1d-4869-820d-a5b454cfba0b/ANAPTYSBIO-INC"


def write_site(site):
    job_response = requests.get(site)
    with open('website.html', 'w') as file:
        file.write(job_response.text)


# write_site(job_url)

with open('website.html') as f:
    data = f.read()
soup = BeautifulSoup(data, 'html.parser')
job_titles = soup.find_all()


