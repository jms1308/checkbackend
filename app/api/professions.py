from flask import Blueprint, request, jsonify
from app.models.profession import Profession, ProfessionType
from app.extensions import db
from app.auth import admin_required

bp = Blueprint('professions', __name__)

@bp.route('', methods=['POST'])
@admin_required
def create_profession():
    data = request.get_json()
    try:
        new_profession = Profession(
            name=data['name'], 
            type=ProfessionType(data['type']),
            amount=data['amount']
        )
        db.session.add(new_profession)
        db.session.commit()
        return jsonify(id=new_profession.id, name=new_profession.name), 201
    except (ValueError, KeyError) as e:
        return jsonify(message=f"Invalid input: {e}"), 400

@bp.route('', methods=['GET'])
@admin_required
def get_professions():
    professions = Profession.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'type': p.type.value, 'amount': p.amount} for p in professions])
