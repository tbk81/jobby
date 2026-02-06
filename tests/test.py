import csv
from src.db_manager import *

# add_company("Erasca", "https://www.erasca.com/open-positions/")
# remove_company("Erasca")
# list_companies()

# add_job("Erasca", "VP Global Pharmacovigilance", "San Diego, CA or remote",
#         "https://www.erasca.com/jobs/vp-global-pharmacovigilance/")

datarows = []
with open("companies.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
       datarows.append(row)
for row in datarows[1:]:
    print(row)