from bs4 import BeautifulSoup

# with open('/Users/trevor/jobby/html_data/erasca.html') as file:
with open('/home/trevor/python-projects/jobby/html_data/erasca.html') as file:
    erasca_data = file.read()
soup = BeautifulSoup(erasca_data, 'html.parser')

job_titles = soup.find_all('div', class_='title-contaier')
job_locations = soup.find_all('div', class_='info-container')
job_urls = soup.find_all('a', class_='job-link')


for i in range(len(job_titles)):
    print(job_titles[i].text.strip())
    print(job_locations[i].get_text(strip=True).replace('→', ''))
    print(job_urls[i]['href'].strip())
    # print("\n")
