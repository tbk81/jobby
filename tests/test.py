from bs4 import BeautifulSoup
from src.site_scraper import write_site

URL = "https://neomorph.com/careers.html"
NAME = "neomorph"
write_site(URL, NAME)
# scraped_data = []
with open(f"'src/html_data/{NAME}.html'") as file:
    data = file.read()
soup = BeautifulSoup(data, 'html.parser')

# job_titles = soup.find_all('div', class_='title-contaier')
# job_locations = soup.find_all('div', class_='info-container')
# job_urls = soup.find_all('a', class_='job-link')
#
# for i in range(len(job_titles)):
#     title = job_titles[i].text.strip()
#     location = job_locations[i].get_text(strip=True)
#     job_url = job_urls[i]['href'].strip()
