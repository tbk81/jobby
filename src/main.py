import os
import importlib
from flask import Flask, jsonify, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, select
from sqlalchemy.sql import func
from datetime import date

SECRET_KEY = os.environ.get("SECRET_KEY")

# SETUP PATHS
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "databases")

# Paths for your two separate files
companies_db_path = os.path.join(DB_FOLDER, "companies.db")
jobs_db_path = os.path.join(DB_FOLDER, "jobs.db")

# CONFIGURE FLASK
app = Flask(__name__)

# Secret key for using flash
app.secret_key = SECRET_KEY

# The "Default" database (Companies)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{companies_db_path}"

# The other databases (Jobs). This can allow for multiple database files
# Give name/key: 'job_db'
app.config["SQLALCHEMY_BINDS"] = {
    "job_db": f"sqlite:///{jobs_db_path}"
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# DEFINE MODELS

class Company(db.Model):
    # No bind key needed, uses the default SQLALCHEMY_DATABASE_URI
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())


class Job(db.Model):
    # Tells Flask to use the 'job_db' file defined in BINDS
    __bind_key__ = "job_db"
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())


# CREATE TABLES
# This will create 'companies' in companies.db and 'jobs' in jobs.db automatically
with app.app_context():
    db.create_all()
    print("Connected to all databases.")


# ROUTES

@app.route('/')
def home():
    # READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database.
    # job_result = db.session.execute(db.select(Job).order_by(Job.company))
    company_result = db.session.execute(db.select(Company).order_by(Company.name))

    # Use .scalars() to get the elements than entire rows from the database.
    # all_jobs = job_result.scalars().all()
    all_companies = company_result.scalars().all()
    # Check if the URL has a company filter (e.g., /?company=Google)
    scraped_company = request.args.get('company')

    if scraped_company:
        # Jobs for the company that was just scraped
        display_jobs = db.session.execute(
            select(Job).where(Job.company == scraped_company)
        ).scalars().all()
    else:
        # If no company is selected (first time loading the page), show an empty list
        # (or change this to select(Job) if you prefer to see all jobs by default)
        display_jobs = []

    return render_template('index.html', all_companies=all_companies, all_jobs=display_jobs, scraped_company=scraped_company)
    # return render_template('index.html', all_jobs=all_jobs, all_companies=all_companies)


@app.route('/company-li')
def company_li():
    # READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database.
    company_result = db.session.execute(db.select(Company).order_by(Company.name))

    # Use .scalars() to get the elements than entire rows from the database.
    all_companies = company_result.scalars().all()
    return render_template('companies.html', all_companies=all_companies)


@app.route('/add_company', methods=['POST'])
def add_company():
    name = request.form.get('company_name')
    url = request.form.get('company_url')

    existing = db.session.execute(select(Company).where(Company.name == name)).scalar_one_or_none()

    if existing:
        # Flash an error message
        flash(f"Error: {name} is already in the database!", "error")
    else:
        new_company = Company(name=name, url=url)
        db.session.add(new_company)
        db.session.commit()
        # Flash a success message
        flash(f"Success! {name} has been added.", "success")

    return redirect('/')

@app.route('/process_selection', methods=['POST'])
def process_selection():
    selected_company = request.form.get('company_name')

    if not selected_company:
        flash("Error: Please select a company first.", "error")
        return redirect('/')

    # Get the company URL from the database
    company = db.session.execute(
        select(Company).where(Company.name == selected_company)
    ).scalar_one_or_none()

    if not company:
        flash("Error: Company not found in database.", "error")
        return redirect('/')

    # Dynamically load the correct parser script
    # e.g., "Eli Lilly" becomes "eli_lilly"
    module_name = selected_company.lower().replace(" ", "_")

    try:
        # Look in the job_parsers folder for the module
        parser = importlib.import_module(f"job_parsers.{module_name}")

        # Run the scraper function and pass the URL
        jobs_found = parser.scrape_jobs(company.url)

        # Save new jobs to the database
        new_jobs_count = 0
        for job in jobs_found:
            # Check if this exact job at this company already exists
            existing_job = db.session.execute(
                select(Job).where(Job.company == selected_company, Job.title == job['title'])
            ).scalar_one_or_none()

            if not existing_job:
                new_job = Job(
                    company=selected_company,
                    title=job['title'],
                    location=job['location'],
                    url=job['url']
                )
                db.session.add(new_job)
                new_jobs_count += 1

        db.session.commit()

        # Flash success message
        flash(f"Success! Scraped {len(jobs_found)} jobs. Added {new_jobs_count} new ones to the board.", "success")

    except ModuleNotFoundError:
        flash(f"Error: Could not find a script named '{module_name}.py' in the job_parsers folder.", "error")
    except Exception as e:
        flash(f"An error occurred while scraping: {str(e)}", "error")
        print(f"An error occurred while scraping: {str(e)}", "error")

    # Redirect to the home page to see the updated jobs
    return redirect(url_for('home', company=selected_company))


if __name__ == "__main__":
    app.run(debug=True)
