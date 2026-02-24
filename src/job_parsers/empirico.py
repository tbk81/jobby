from bs4 import BeautifulSoup
from src.site_scraper import write_site

def scrape_jobs(url):
    write_site(url, "empirico")
    scraped_data = []
    with open('src/html_data/empirico.html') as file:
        empirico_data = file.read()
    soup = BeautifulSoup(empirico_data, 'html.parser')

    job_titles = soup.find_all('h3')
    job_locations = soup.find_all('div', class_='location')

    for i in range(len(job_titles)-1):
        title = job_titles[i].text.strip()
        location = job_locations[i].get_text(strip=True)
        job_url = "https://www.empiri.co/careers/"
        print("\n")

        scraped_data.append({
            "title": title,
            "location": location,
            "url": job_url
        })

    return scraped_data
