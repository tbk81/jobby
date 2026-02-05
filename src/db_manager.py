# import sqlite3
from Cython.Shadow import nonecheck
from sqlalchemy import Integer, String, Date, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from datetime import date

# companies_db_cursor.execute("CREATE TABLE companies (id INTEGER PRIMARY KEY, company varchar(250) "
#                             "NOT NULL UNIQUE, url varchar(250) NOT NULL, date )")

# companies_db = sqlite3.connect('databases/companies.db')
# companies_db_cursor = companies_db.cursor()
# new_column = "ALTER TABLE companies ADD COLUMN date_added TIMESTAMP"
# companies_db_cursor.execute(new_column)
# delete_column = "ALTER TABLE companies DROP COLUMN addDate"
# companies_db_cursor.execute(delete_column)

class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())  # automatically creates the date


# Connect the database
engine = create_engine("sqlite:///databases/companies.db")
Base.metadata.create_all(engine)
# print("Table 'companies' created successfully.")


def list_companies():
    with Session(engine) as session:
        companies = session.scalars(select(Company)).all()
        print(f"\nCurrent DB: {[c.name for c in companies]}")

def add_company(name, url):
    """
    Adds a new company to the database.

    Args:
        name (str): The name of the company.
        url (str): The website URL.
    """
    # with Session(engine) as session:
    #     new_company = Company(name=name, url=url)
    #     session.add(new_company)
    #     session.commit()
    #     print(f"Success: Added '{name}'")

    with Session(engine) as session:
        try:
            new_company = Company(
                name=name,
                url=url
            )
            session.add(new_company)
            session.commit()
            print(f"Success: Added '{name}' to the database.")
            return new_company
        except IntegrityError:
            # This block runs if the name already exists (unique constraint violation)
            session.rollback()  # Cancel the pending transaction
            print(f"Error: The company '{name}' already exists.")
            return None
        except Exception as e:
            # Catch any other unexpected errors
            session.rollback()
            print(f"An unexpected error occurred: {e}")
            return None

def remove_company(name):
    with Session(engine) as session:
        # Find the company, scalar_one_or_none() returns the object if found, or None if not
        stmt = select(Company).where(Company.name == name)
        company_to_delete = session.execute(stmt).scalar_one_or_none()
        # Check and Delete
        if company_to_delete:
            session.delete(company_to_delete)
            session.commit()
            print(f"Success: Deleted '{name}' from the database.")
        else:
            print(f"Warning: Could not delete '{name}' because it does not exist.")
