import os
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, select
from sqlalchemy.sql import func
from datetime import date

# SETUP PATHS
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "databases")

# Paths for your two separate files
companies_db_path = os.path.join(DB_FOLDER, "companies.db")
jobs_db_path = os.path.join(DB_FOLDER, "jobs.db")

# CONFIGURE FLASK
app = Flask(__name__)

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
    # No bind key needed -> uses the default SQLALCHEMY_DATABASE_URI
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
# @app.route('/')
# def show_all():
#     # Query both db's
#     companies = db.session.execute(select(Company)).scalars().all()
#     jobs = db.session.execute(select(Job)).scalars().all()
#
#     return jsonify({
#         "total_companies": len(companies),
#         "total_jobs": len(jobs),
#         "companies": [c.name for c in companies],
#         "jobs": [j.company + "  " + j.title for j in jobs]
#     })

@app.route('/')
def home():
    # READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database.
    job_result = db.session.execute(db.select(Job).order_by(Job.company))

    # Use .scalars() to get the elements than entire rows from the database.
    all_jobs = job_result.scalars().all()
    return render_template('index.html', all_jobs=all_jobs)


if __name__ == "__main__":
    app.run(debug=True)
