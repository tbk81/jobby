from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import create_engine, Integer, String, Float

app = Flask(__name__)


# class Base(DeclarativeBase):
#     pass
# db = SQLAlchemy(model_class=Base)
# configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
company_engine = create_engine("sqlite:///src/databases/companies.db")
job_engine = create_engine(f"sqlite:///src/databases/jobs.db")

company_session = sessionmaker(bind=company_engine)
company_session = company_session()

job_session = sessionmaker(bind=job_engine)
job_session = job_session()

company_base = declarative_base()
job_base = declarative_base()

db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # When creating new records, the primary key
    # fields is optional. The id field will be auto-generated.
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # This will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'





if __name__ == "__main__":
    app.run(debug=True)



# ---------------------------------------------- TESTING ---------------------------------------------- #

# @app.route("/add", methods=['GET', 'POST'])
# def add():
#     if request.method == 'POST':
#         new_book = {
#             "title": request.form["title"],
#             "author": request.form["author"],
#             "rating": request.form["rating"],
#         }
#         all_books.append(new_book)
#         return redirect(url_for('home'))
#     return render_template('add.html')




