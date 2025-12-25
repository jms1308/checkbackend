from flask import Blueprint, request, jsonify
from app.models.employee import Employee, DailyHours
from app.extensions import db
from app.auth import admin_required
from datetime import datetime

bp = Blueprint('employees', __name__)

@bp.route('', methods=['POST'])
@admin_required
def create_employee():
    data = request.get_json()
    new_employee = Employee(
        first_name=data['first_name'], 
        last_name=data['last_name'],
        profession_id=data['profession_id']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(id=new_employee.id), 201

@bp.route('/<int:id>/hours', methods=['POST'])
@admin_required
def record_hours():
    data = request.get_json()
    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        daily_hours = DailyHours(
            employee_id=id,
            date=date,
            hours=data['hours']
        )
        db.session.add(daily_hours)
        db.session.commit()
        return jsonify(id=daily_hours.id), 201
    except (ValueError, KeyError):
        return jsonify(message="Invalid data"), 400
