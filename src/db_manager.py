# import sqlite3
import os
from sqlalchemy import Integer, String, Date, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from datetime import date


class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())  # automatically creates the date


# Connect the database
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory where THIS file (db_manager.py) is located
# DB_PATH = os.path.join(BASE_DIR, "databases", "companies.db") # Construct the absolute path to the database file
# engine = create_engine(f"sqlite:///{DB_PATH}")  # Create the engine using the absolute path
# print(f"Connecting to database at: {DB_PATH}")
engine = create_engine(f"sqlite:///src/databases/companies.db")  # Create the engine using the absolute path
print("Connecting to database at: companies.db")
Base.metadata.create_all(engine)


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
