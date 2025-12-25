from flask import Blueprint, request, jsonify
from app.models.test_result import TestResult
from app.extensions import db
from app.auth import admin_required
from datetime import datetime

bp = Blueprint('test_results', __name__)

@bp.route('', methods=['POST'])
@admin_required
def create_test_result():
    data = request.get_json()
    try:
        new_test_result = TestResult(
            student_id=data['student_id'],
            subject=data['subject'],
            score=data['score'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        db.session.add(new_test_result)
        db.session.commit()
        return jsonify(id=new_test_result.id), 201
    except (ValueError, KeyError):
        return jsonify(message="Invalid data"), 400
