"""
application.py
- creates a Flask app instance and registers the database object
"""

from flask import Flask
from flask_cors import CORS

def create_app(app_name='near_u'):
    app = Flask(app_name)
    app.config.from_object('near_u.config')
    CORS(app, resources={r'/*': {'origins': '*'}})
    from near_u.api import api

    app.register_blueprint(api, url_prefix="/api")

    from near_u.models import db
    db.init_app(app)

    return app

