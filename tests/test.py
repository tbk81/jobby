import csv
from src.db_manager import *

add_company("Erasca", "https://www.erasca.com/open-positions/")
# remove_company("Erasca")
list_companies()

# add_job("Erasca", "VP Global Pharmacovigilance", "San Diego, CA or remote",
#         "https://www.erasca.com/jobs/vp-global-pharmacovigilance/")


# Used to populate the db from a csv file
# data_rows = []
# with open("companies.csv", 'r') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         data_rows.append(row)
# for row in data_rows[1:]:
#     print(row)

# remove_job("VP Global Pharmacovigilance")
# list_job_titles()
