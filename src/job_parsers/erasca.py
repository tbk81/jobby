from bs4 import BeautifulSoup
from src.site_scraper import write_site

def scrape_jobs(url):
    write_site(url, "erasca")
    scraped_data = []
    with open('src/html_data/erasca.html') as file:
        erasca_data = file.read()
    soup = BeautifulSoup(erasca_data, 'html.parser')

    job_titles = soup.find_all('div', class_='title-contaier')
    job_locations = soup.find_all('div', class_='info-container')
    job_urls = soup.find_all('a', class_='job-link')

    for i in range(len(job_titles)):
        title = job_titles[i].text.strip()
        location = job_locations[i].get_text(strip=True).replace('→', '')
        job_url = job_urls[i]['href'].strip()

        scraped_data.append({
            "title": title,
            "location": location,
            "url": job_url
        })

    return scraped_data
