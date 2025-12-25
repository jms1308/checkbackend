from app.extensions import db
from sqlalchemy import func

class StudentPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=func.now())
    is_monthly_fee = db.Column(db.Boolean, nullable=False, default=False)

    student = db.relationship('Student', back_populates='payments')
