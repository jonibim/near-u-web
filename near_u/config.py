"""
config.py
- settings for the flask application object
"""

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# used for encryption and session management
SECRET_KEY = 'mysecretkey'