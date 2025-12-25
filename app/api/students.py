from flask import Blueprint, request, jsonify
from app.models.student import Student
from app.models.student_payment import StudentPayment
from app.extensions import db
from app.auth import admin_required
from datetime import datetime
from sqlalchemy import extract, func

bp = Blueprint('students', __name__)

@bp.route('', methods=['POST'])
@admin_required
def create_student():
    data = request.get_json()
    try:
        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            grade=data.get('grade'),
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            monthly_fee=data.get('monthly_fee', 0)
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify(id=new_student.id), 201
    except (ValueError, KeyError):
        return jsonify(message="Invalid data"), 400

@bp.route('/<int:id>/payment', methods=['POST'])
@admin_required
def record_payment(id):
    data = request.get_json()
    student = Student.query.get_or_404(id)
    try:
        payment = StudentPayment(
            student_id=id,
            amount=data['amount'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        student.balance += data['amount']
        db.session.add(payment)
        db.session.commit()
        return jsonify(balance=student.balance)
    except (ValueError, KeyError):
        return jsonify(message="Invalid data"), 400

@bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'grade': student.grade,
        'date_of_birth': student.date_of_birth.isoformat(),
        'balance': student.balance,
        'monthly_fee': student.monthly_fee
    })

@bp.route('/earnings', methods=['GET'])
@admin_required
def get_earnings():
    month = request.args.get('month')

    if not month:
        return jsonify(message="Month is required"), 400

    try:
        month_date = datetime.strptime(month, '%Y-%m').date()
    except ValueError:
        return jsonify(message="Invalid month format. Use YYYY-MM"), 400

    total_earnings = db.session.query(
        func.sum(StudentPayment.amount)
    ).filter(
        extract('year', StudentPayment.date) == month_date.year,
        extract('month', StudentPayment.date) == month_date.month
    ).scalar()

    return jsonify(total_earnings=float(total_earnings) if total_earnings else 0)
