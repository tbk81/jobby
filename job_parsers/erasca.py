from bs4 import BeautifulSoup

# with open('/Users/trevor/jobby/html_data/erasca.html') as file:
with open('/home/trevor/python-projects/jobby/html_data/erasca.html') as file:
    erasca_data = file.read()
soup = BeautifulSoup(erasca_data, 'html.parser')

job_titles = soup.find_all('div', class_='title-contaier')
job_locations = soup.find_all('div', class_='job-location')
job_urls = soup.find_all('div', class_='job-link')
for title in job_titles:
    print(title.text.strip())
