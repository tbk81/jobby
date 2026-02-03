from csv import writer, reader

# Returns companies url from the csv file for parsing
def url_grabber(company_name):
    with open('/Users/trevor/jobby/companies.csv', newline='') as csv_file:
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
    with open('companies.csv', 'a', newline='') as f:
        f.write('\n')
        writer_obj = writer(f)
        writer_obj.writerow(company)

