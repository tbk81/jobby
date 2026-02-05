from bs4 import BeautifulSoup

with open('html_data/empirico.html') as file:
    empirico_data = file.read()
soup = BeautifulSoup(empirico_data, 'html.parser')

job_titles = soup.find_all('h3')
job_locations = soup.find_all('div', class_='location')

for i in range(len(job_titles)-1):
    print(job_titles[i].text.strip())
    print(job_locations[i].get_text(strip=True))
    print("https://www.empiri.co/careers/")
    print("\n")
