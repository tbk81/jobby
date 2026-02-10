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

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())


# Connect the databases
company_engine = create_engine(f"sqlite:///src/databases/companies.db")  # Create the engine using the absolute path
Base.metadata.create_all(company_engine)

job_engine = create_engine(f"sqlite:///src/databases/jobs.db")
Base.metadata.create_all(job_engine)



# --------------------------------------- Company db functions --------------------------------------- #
def list_companies():
    with Session(company_engine) as session:
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

    with Session(company_engine) as session:
        # Checks if specific company exists
        stmt = select(Company).where(
            Company.name == name,
        )
        existing_company = session.execute(stmt).scalar_one_or_none()

        if existing_company:
            print(f"Skipping: Job '{name}' already exists.")
            return None

        try:
            new_company = Company(
                name=name,
                url=url
            )
            session.add(new_company)
            session.commit()
            print(f"Success: Added '{name}'")
            return new_company

        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred: {e}")
            return None

def remove_company(name):
    with Session(company_engine) as session:
        # Find the company, scalar_one_or_none() returns the object if found, or None if not
        stmt = select(Company).where(Company.name == name)
        company_to_delete = session.execute(stmt).scalar_one_or_none()
        # Check and Delete
        if company_to_delete:
            session.delete(company_to_delete)
            session.commit()
            print(f"Success: Deleted '{name}' from the company database.")
        else:
            print(f"Warning: Could not delete '{name}' because it does not exist.")


def get_company_url(name):
    """
    Searches for a company by name and returns its URL.
    Returns None if the company is not found.
    """
    with Session(company_engine) as session:
        # Select ONLY the 'url' column where the name matches
        stmt = select(Company.url).where(Company.name == name)
        # .scalar() returns the single value (the string) directly
        # If no row is found, it returns None automatically
        url = session.execute(stmt).scalar()

        return url



# --------------------------------------- job db functions --------------------------------------- #
def list_job_titles():
    with Session(job_engine) as session:
        jobs = session.scalars(select(Job)).all()
        print(f"\nCurrent job title: {[j.title for j in jobs]}")

def add_job(company, title, location, url):
    """
        Adds a new job posting to the jobs database.

        Args:
            company (str): Company name.
            title (str): Job title.
            location (str): Location of the job posting.
            url (str): Job posting url.
    """
    with Session(job_engine) as session:
        # Checks if specific job at this company exists
        stmt = select(Job).where(
            Job.company == company,
            Job.title == title
        )
        existing_job = session.execute(stmt).scalar_one_or_none()

        if existing_job:
            print(f"Skipping: Job '{title}' at '{company}' already exists.")
            return None
        try:
            new_job = Job(
                company=company,
                title=title,
                location=location,
                url=url
            )
            session.add(new_job)
            session.commit()
            print(f"Success: Added '{title}' to the jobs database.")
            return new_job
        except IntegrityError:
            # This block runs if the job title already exists (unique constraint violation)
            session.rollback()  # Cancel the pending transaction
            print(f"Error: The job '{title}' already exists.")
            return None
        except Exception as e:
            # Catch any other unexpected errors
            session.rollback()
            print(f"An unexpected error occurred: {e}")
            return None

def remove_job(title):
    with Session(job_engine) as session:
        # Find the job title, scalar_one_or_none() returns the object if found, or None if not
        stmt = select(Job).where(Job.title == title)
        title_to_delete = session.execute(stmt).scalar_one_or_none()
        # Check and Delete
        if title_to_delete:
            session.delete(title_to_delete)
            session.commit()
            print(f"Success: Deleted '{title}' from the company database.")
        else:
            print(f"Warning: Could not delete '{title}' because it does not exist.")
