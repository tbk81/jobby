from bs4 import BeautifulSoup

# for testing how to parse the job titles and descriptions
def title_parser():
    with open('html_data/website.html') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'html.parser')
    job_titles = soup.find_all('div')
    print(job_titles)


with open('/Users/trevor/jobby/html_data/erasca.html') as file:
    erasca_data = file.read()
test_soup = BeautifulSoup(erasca_data, 'html.parser')
# print(test_soup.find_all(class_='title-contaier'))
# print(test_soup.find_all(name='span'))
spans = test_soup.find_all(name='span')
count = 0
for s in spans:
    count += 1
    print(f'{s}\t{s.text}\t{count}')
for s in spans:
    if "data-v-638fa1cc" in s:
        print(s.text)


