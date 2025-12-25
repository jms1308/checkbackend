import enum
from app.extensions import db

class ProfessionType(enum.Enum):
    HOURLY = 'hourly'
    MONTHLY = 'monthly'

class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.Enum(ProfessionType), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    employees = db.relationship('Employee', backref='profession', lazy=True)
