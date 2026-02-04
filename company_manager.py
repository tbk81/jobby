from path_finder import companies_path
from csv import writer, reader

path_to_companies = companies_path()

# Returns companies url from the csv file for parsing
def url_grabber(company_name):
    with open(path_to_companies, newline='') as csv_file:
        csv_reader = reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == company_name:
                company_url = " ".join(row).split(" ")[1]
                break
            else:
                company_url = "Not found"
        return company_url

# Adds a new company/url to the csv file
def add_company(company):
    with open(path_to_companies, 'a', newline='') as f:
        f.write('\n')
        writer_obj = writer(f)
        writer_obj.writerow(company)

