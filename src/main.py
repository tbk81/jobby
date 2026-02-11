import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, select
from sqlalchemy.sql import func
from datetime import date

# --- 1. SETUP PATHS ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "databases")

# Paths for your two separate files
companies_db_path = os.path.join(DB_FOLDER, "companies.db")
jobs_db_path = os.path.join(DB_FOLDER, "jobs.db")

# --- 2. CONFIGURE FLASK ---
app = Flask(__name__)

# The "Default" database (Companies)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{companies_db_path}"

# The "Extra" databases (Jobs)
# We give this one a name/key: 'job_db'
app.config["SQLALCHEMY_BINDS"] = {
    "job_db": f"sqlite:///{jobs_db_path}"
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# --- 3. DEFINE MODELS ---

class Company(db.Model):
    # No bind key needed -> uses the default SQLALCHEMY_DATABASE_URI
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())


class Job(db.Model):
    # This magic line tells Flask to use the 'job_db' file defined in BINDS
    __bind_key__ = "job_db"
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    date_added: Mapped[date] = mapped_column(Date, default=func.current_date())


# --- 4. CREATE TABLES ---
# This will create 'companies' in companies.db and 'jobs' in jobs.db automatically
with app.app_context():
    db.create_all()
    print("Connected to both databases.")


# --- 5. ROUTES ---
@app.route('/all-data')
def show_all():
    # We can query both seamlessly
    companies = db.session.execute(select(Company)).scalars().all()
    jobs = db.session.execute(select(Job)).scalars().all()

    return jsonify({
        "total_companies": len(companies),
        "total_jobs": len(jobs),
        "companies": [c.name for c in companies],
        "jobs": [j.company + "  " + j.title for j in jobs]
    })


if __name__ == "__main__":
    app.run(debug=True)
