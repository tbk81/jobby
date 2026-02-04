import sqlite3
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

companies_db = sqlite3.connect('databases/companies.db')
companies_db_cursor = companies_db.cursor()

companies_db_cursor.execute("CREATE TABLE companies (id INTEGER PRIMARY KEY, company varchar(250) "
                            "NOT NULL UNIQUE, url varchar(250) NOT NULL, date )")

class Book(db.Model):
    company: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[float] = mapped_column(Float, nullable=False)

    # This will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'
