from bs4 import BeautifulSoup

# with open('/Users/trevor/jobby/html_data/anaptysbio.html') as file:
with open('/home/trevor/python-projects/jobby/html_data/anaptysbio.html') as file:
    anaptys_data = file.read()
soup = BeautifulSoup(anaptys_data, 'html.parser')

job_titles = soup.find_all('a', class_='no-underline custom-link-color')
job_locations = soup.find_all('span', style='line-height: 1.33;')
job_urls = soup.find_all('a', class_='no-underline custom-link-color')


for i in range(len(job_titles)):
    print(job_titles[i].text.strip())
    print(job_locations[i].get_text(strip=True))
    print(f'https://recruiting.paylocity.com{job_urls[i]['href'].strip()}')
#     print("\n")