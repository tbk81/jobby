from bs4 import BeautifulSoup
from src.site_scraper import write_site


def scrape_jobs(url):
    write_site(url, "janux")
    scraped_data = []
    with open('src/html_data/janux.html') as file:
        janux_data = file.read()
    soup = BeautifulSoup(janux_data, 'html.parser')

    job_titles = soup.find_all('h5')
    job_locations = soup.find_all('span', class_='sort-by-location posting-category small-category-label location')
    job_urls = soup.find_all('a', class_='posting-btn-submit template-btn-submit cerulean')

    for i in range(len(job_titles)):
        title = job_titles[i].text.strip()
        location = job_locations[i].get_text(strip=True)
        job_url = job_urls[i]['href'].strip()

        scraped_data.append({
            "title": title,
            "location": location,
            "url": job_url
        })

    return scraped_data
