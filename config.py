import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = r"postgresql://postgres:postgres@localhost:5432/fyyurdb"

# Connect to the database
from sqlalchemy import create_engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

