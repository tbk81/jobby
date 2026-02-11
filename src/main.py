from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, select
from sqlalchemy.sql import func
from datetime import date
# import os

# --- 1. SETUP FLASK & DATABASE ---
app = Flask(__name__)

# Ensure the "databases" folder exists
# if not os.path.exists("databases"):
#     os.makedirs("databases")

# Configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databases/job_board.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the Database Extension
db = SQLAlchemy(app)


# --- 2. DEFINE MODELS ---
# In Flask, we inherit from db.Model instead of creating our own Base

class Company(db.Model):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())


class Job(db.Model):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(250), nullable=False)  # Storing company name as string
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())


# --- 3. HELPER FUNCTIONS (Refactored for Flask) ---

def add_company_to_db(name, url):
    """Adds a company if it doesn't exist."""
    # We use db.session directly now
    existing = db.session.execute(select(Company).where(Company.name == name)).scalar_one_or_none()

    if existing:
        return f"Skipped: {name} already exists."

    new_company = Company(name=name, url=url)
    db.session.add(new_company)
    db.session.commit()
    return f"Success: Added {name}"


def add_job_to_db(company, title, location, url):
    """Adds a job if (Company + Title) doesn't exist."""
    existing = db.session.execute(
        select(Job).where(Job.company == company, Job.title == title)
    ).scalar_one_or_none()

    if existing:
        return f"Skipped: {title} at {company} already exists."

    new_job = Job(company=company, title=title, location=location, url=url)
    db.session.add(new_job)
    db.session.commit()
    return f"Success: Added {title}"


# --- 4. FLASK ROUTES (Web Interface) ---

@app.route('/')
def home():
    return "<h1>Job Board API is Running</h1><p>Go to /jobs or /companies to see data.</p>"


@app.route('/companies')
def list_companies():
    # Fetch all companies
    companies = db.session.execute(select(Company)).scalars().all()
    # Convert to a list of dictionaries (JSON)
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "url": c.url,
        "date": str(c.date_added)
    } for c in companies])


@app.route('/jobs')
def list_jobs():
    jobs = db.session.execute(select(Job)).scalars().all()
    return jsonify([{
        "company": j.company,
        "title": j.title,
        "location": j.location,
        "url": j.url
    } for j in jobs])


# --- 5. RUN THE APP ---
if __name__ == "__main__":
    # This creates the tables if they don't exist yet
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")

        # Optional: Add dummy data for testing
        print(add_company_to_db("Google", "https://google.com"))
        print(add_job_to_db("Google", "Software Engineer", "Mountain View, CA", "https://google.com/careers"))

    # Start the server
    app.run(debug=True)