import os

LINUX = "posix"
MACOS = "darwin"
LINUX_PATH = "/home/trevor/python-projects/jobby/companies.csv"
MACOS_PATH = "/Users/trevor/jobby/companies.csv"

if os.path.exists(LINUX_PATH):
    csv_path = LINUX_PATH
else:
    csv_path = MACOS_PATH
