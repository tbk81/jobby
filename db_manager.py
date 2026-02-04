from path_finder import database_path
import sqlite3
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

path_to_db = database_path()

companies_db = sqlite3.connect(f'{path_to_db}companies.db')
companies_db_cursor = companies_db.cursor()


