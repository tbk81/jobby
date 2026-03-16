import os
import importlib
from flask import Flask, render_template, request, redirect, flash, url_for
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
stats_db_path = os.path.join(DB_FOLDER, "stats.db")

# CONFIGURE FLASK
app = Flask(__name__)

# Secret key for using flash
app.secret_key = SECRET_KEY

# The "Default" database (Companies)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{companies_db_path}"

# The other databases (Jobs). This can allow for multiple database files
# Give name/key: 'job_db'
app.config["SQLALCHEMY_BINDS"] = {
    "job_db": f"sqlite:///{jobs_db_path}",
    "stats_db": f"sqlite:///{stats_db_path}"
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# DEFINE MODELS

class Company(db.Model):
    # Use the default SQLALCHEMY_DATABASE_URI
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())


class Job(db.Model):
    # Tells Flask to use the 'job_db' file defined in binds
    __bind_key__ = "job_db"
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())
    date_updated: Mapped[date] = mapped_column(Date, default=func.current_date())


class StatsJob(db.Model):
    # Tells Flask to save in stats.db
    __bind_key__ = "stats_db"
    __tablename__ = "historical_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Copies the original date it was found
    date_added: Mapped[date] = mapped_column(Date)

    # Stamps the date it was moved to this database (job closed)
    date_removed: Mapped[date] = mapped_column(Date, default=func.current_date())


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
    company_result = db.session.execute(db.select(Company).order_by(Company.name))

    # Use .scalars() to get the elements than entire rows from the database.
    all_companies = company_result.scalars().all()
    # Check if the URL has a company filter (e.g., /?company=Google)
    scraped_company = request.args.get('company')

    if scraped_company:
        # Jobs for the company that was just scraped
        display_jobs = db.session.execute(
            select(Job).where(Job.company == scraped_company)).scalars().all()
    else:
        # If no company is selected (first time loading the page), show an empty list
        # (or change this to select(Job) if you prefer to see all jobs by default)
        display_jobs = []

    return render_template('index.html',
                           all_companies=all_companies,
                           all_jobs=display_jobs,
                           scraped_company=scraped_company,
                           today=date.today()
                           )


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

    # 1. Determine which companies to scrape
    if selected_company == "ALL":
        companies_to_scrape = db.session.execute(select(Company)).scalars().all()
    else:
        # Just grab the single selected company
        single_comp = db.session.execute(
            select(Company).where(Company.name == selected_company)
        ).scalar_one_or_none()

        if not single_comp:
            flash("Error: Company not found in database.", "error")
            return redirect('/')
        companies_to_scrape = [single_comp]

    # Tracking variables for the flash message
    total_new_jobs = 0
    total_moved_jobs = 0
    total_scraped = 0
    errors = []

    from datetime import date

    # 2. Loop through the list of companies
    for comp in companies_to_scrape:
        module_name = comp.name.lower().replace(" ", "_")

        try:
            # Dynamically load the correct parser script
            parser = importlib.import_module(f"job_parsers.{module_name}")
            jobs_found = parser.scrape_jobs(comp.url)
            total_scraped += len(jobs_found)

            # --- COMPARISON LOGIC ---
            scraped_titles = [job.get('title') for job in jobs_found if job.get('title')]

            existing_jobs = db.session.execute(
                select(Job).where(Job.company == comp.name)
            ).scalars().all()

            # Find stale jobs and move them
            for old_job in existing_jobs:
                if old_job.title not in scraped_titles:
                    historical_job = StatsJob(
                        company=old_job.company,
                        title=old_job.title,
                        location=old_job.location,
                        url=old_job.url,
                        date_added=old_job.date_added
                    )
                    db.session.add(historical_job)
                    db.session.delete(old_job)
                    total_moved_jobs += 1

            # Process newly scraped jobs
            for job in jobs_found:
                job_title = job.get('title')
                if not job_title:
                    continue

                existing_job = db.session.execute(
                    select(Job).where(Job.company == comp.name, Job.title == job_title)
                ).scalar_one_or_none()

                if not existing_job:
                    new_job = Job(
                        company=comp.name,
                        title=job_title,
                        location=job.get('location', 'Remote/Unspecified'),
                        url=job.get('url') or "No link available"
                    )
                    db.session.add(new_job)
                    total_new_jobs += 1
                else:
                    existing_job.date_updated = date.today()

            # Commit the database changes for THIS company before moving to the next
            db.session.commit()

        except ModuleNotFoundError:
            errors.append(f"Skipped {comp.name}: Missing '{module_name}.py' script.")
        except Exception as e:
            db.session.rollback()  # Undo any pending DB changes for this specific company if it crashes
            errors.append(f"Error scraping {comp.name}: {str(e)}")

    # 3. Handle Flash Messages and Redirection
    if errors:
        # If any company failed, flash the specific errors
        for err in errors:
            flash(err, "error")

    if selected_company == "ALL":
        flash(
            f"Bulk scrape complete! Scraped {total_scraped} total jobs. Added {total_new_jobs} new. Moved {total_moved_jobs} to stats.",
            "success")
        # Redirect to the main home page (shows an empty job board so they can choose what to look at)
        return redirect(url_for('home'))
    else:
        flash(
            f"Success! Scraped {total_scraped} jobs for {selected_company}. Added {total_new_jobs} new. Moved {total_moved_jobs} to stats.",
            "success")
        # Redirect back to the filtered view for that specific company
        return redirect(url_for('home', company=selected_company))

@app.route('/stats')
def stats():
    # 1. Fetch all closed jobs, sorting by the date they were removed (newest first)
    closed_jobs = db.session.execute(
        select(StatsJob).order_by(StatsJob.date_removed.desc())
    ).scalars().all()

    # 2. Count the total for a quick metrics display
    total_closed = len(closed_jobs)

    return render_template('stats.html', closed_jobs=closed_jobs, total_closed=total_closed)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
