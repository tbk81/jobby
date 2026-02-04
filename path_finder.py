import os

LINUX = "posix"
MACOS = "darwin"
LINUX_CSV_PATH = "/home/trevor/python-projects/jobby/companies.csv"
LINUX_HTML_PATH = "/home/trevor/python-projects/jobby/html_data/"
MACOS_CSV_PATH = "/Users/trevor/jobby/companies.csv"
MACOS_HTML_PATH = "/Users/trevor/jobby/html_data/"

def companies_path():
    if os.name == LINUX:
        csv_path = LINUX_CSV_PATH
    else:
        csv_path = MACOS_CSV_PATH
    return csv_path

def html_data_path(name):
    if os.name == LINUX:
        html_path = f'{LINUX_HTML_PATH}{name}.html'
    else:
        html_path = f'{MACOS_HTML_PATH}{name}.html'
    return html_path

