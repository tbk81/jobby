import sqlite3
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

companies_db = sqlite3.connect('databases/companies.db')
companies_db_cursor = companies_db.cursor()

# companies_db_cursor.execute("CREATE TABLE companies (id INTEGER PRIMARY KEY, company varchar(250) "
#                             "NOT NULL UNIQUE, url varchar(250) NOT NULL, date )")

# new_column = "ALTER TABLE companies ADD COLUMN addDate TIMESTAMP"
# companies_db_cursor.execute(new_column)

class Company:
    company: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)

def add(name, url):
    new_company = Company(
        company = name,
        url = url,
        date =
    )

