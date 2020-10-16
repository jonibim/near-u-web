"""
models.py
- Data classes for the surveyapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    #surveys= db.relationship('Survey', backref="creator", lazy=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method="sha256")

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)


class Sensor(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    s_type = db.Column(db.String)
    conditions = db.relationship('Condition', backref="sensor", lazy=False)

    def to_dict(self):
        return dict(id=self.id,
                    s_type=self.s_type,
                    conditions=[condition.to_dict() for condition in self.conditions])


class Condition(db.Model):
    __tablename__ = 'conditions'

    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(500), nullable=False)
    c_type = db.Column(db.Integer)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))

    def to_dict(self):
        return dict(id=self.id,
                    condition=self.condition,
                    c_type = self.c_type,
                    sensor_id=self.sensor_id)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    s_type = db.Column(db.String(500), nullable=False)
    condition = db.Column(db.String(500), nullable=False)
    configurations = db.relationship('Configuration', backref='task', lazy=False)
   
    def to_dict(self):
        return dict(id=self.id,
                    title = self.title,
                    s_type=self.s_type,
                    condition=self.condition,
                    configurations=[configuration.to_dict() for configuration in self.configurations])

class Configuration(db.Model):
    __tablename__ = 'configurations'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    notifications = db.Column(db.Boolean, nullable=False)
    repeat = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return dict(id=self.id,
                    task_id = self.task_id,
                    notifications = self.notifications,
                    repeat = self.repeat,
                    addead_at = self.added_at)

