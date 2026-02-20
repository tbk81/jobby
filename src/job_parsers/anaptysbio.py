from bs4 import BeautifulSoup
from src.site_scraper import write_site

def scrape_jobs(url):
    write_site(url, "anaptysbio")
    scraped_data = []
    with open('src/html_data/anaptysbio.html') as file:
        anaptys_data = file.read()
    soup = BeautifulSoup(anaptys_data, 'html.parser')

    job_titles = soup.find_all('a', class_='no-underline custom-link-color')
    job_locations = soup.find_all('span', style='line-height: 1.33;')
    job_urls = soup.find_all('a', class_='no-underline custom-link-color')


    for i in range(len(job_titles)):
        title = job_titles[i].text.strip()
        location = job_locations[i].get_text(strip=True)
        url = f'https://recruiting.paylocity.com{job_urls[i]['href'].strip()}'

        scraped_data.append({
                "title": title,
                "location": location,
                "url": url
        })

    # site_driver.quit()

    return scraped_data
