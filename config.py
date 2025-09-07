import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:9963@localhost:5432/taskcode_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False