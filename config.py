import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

SECRET_KEY = 'd1e60d987206ea0ac373dc4e8df64b7a'

BOOTSTRAP_SERVE_LOCAL = True
