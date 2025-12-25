from app.extensions import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    balance = db.Column(db.Float, nullable=False, default=0)
    monthly_fee = db.Column(db.Float, nullable=False, default=0)
    payments = db.relationship('StudentPayment', back_populates='student')
    test_results = db.relationship('TestResult', backref='student', lazy=True)
