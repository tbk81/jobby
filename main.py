from company_manager import *
from site_scraper import write_site, sel_driver

# new_company = ["Erasca", "https://www.erasca.com/open-positions/"]

# add_company(new_company)
# mira = url_grabber("Mirador")
# print(mira)

# site_data = write_site(url_grabber("Erasca"), "erasca")
# site_data = write_site(url_grabber("Janux"), "Janux")
# site_data = write_site(url_grabber("Empirico"), "empirico")
# site_data = sel_driver(url_grabber("AnaptysBio"), "anaptysbio")
site_data = sel_driver(url_grabber("Mirador"), "mirador")

