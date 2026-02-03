from bs4 import BeautifulSoup

# with open('/Users/trevor/jobby/html_data/mirador.html') as file:
with open('/home/trevor/python-projects/jobby/html_data/janux.html') as file:
    mirador_data = file.read()
soup = BeautifulSoup(mirador_data, 'html.parser')

job_titles = soup.find_all('h5')
job_locations = soup.find_all('span', class_='sort-by-location posting-category small-category-label location')
job_urls = soup.find_all('a', class_='posting-btn-submit template-btn-submit cerulean')

# for i in range(len(job_titles)):
#     print(job_titles[i].text.strip())
#     print(job_locations[i].get_text(strip=True))
#     print(job_urls[i]['href'].strip())
#     print("\n")
