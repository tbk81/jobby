from src.site_scraper import sel_driver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def scrape_jobs(url):
    scraped_data = []
    site_driver = sel_driver(url)
    try:
        button = site_driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    except NoSuchElementException:
        print("Accept cookies button not found")
    else:
        button.click()

    try:
        frame = site_driver.find_element(By.ID, "grnhse_iframe")
        site_driver.switch_to.frame(frame)
        html = site_driver.page_source
    except NoSuchElementException:
        print("element not found")
    else:
        with open('src/html_data/mirador.html', 'w') as file:
            file.write(html)
    site_driver.quit()

    with open('src/html_data/mirador.html') as file:
        mirador_data = file.read()
    soup = BeautifulSoup(mirador_data, 'html.parser')
    #
    job_titles = soup.find_all('p', class_='body body--medium')
    job_locations = soup.find_all('p', class_='body body__secondary body--metadata')
    job_urls = soup.find_all('a')

    for i in range(len(job_titles))[1:]:
        title = job_titles[i].text
        location = job_locations[i - 1].get_text(strip=True)
        job_url = job_urls[i - 1]['href'].strip("#all_jobs")

        scraped_data.append({
            "title": title,
            "location": location,
            "url": job_url
        })

    site_driver.quit()

    return scraped_data

