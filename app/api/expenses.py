from flask import Blueprint, request, jsonify
from app.models.expense import Expense
from app.extensions import db
from app.auth import admin_required
from datetime import datetime
from sqlalchemy import extract, func

bp = Blueprint('expenses', __name__, url_prefix='/api/expenses')

@bp.route('', methods=['POST'])
@admin_required
def create_expense():
    """Create a new expense."""
    data = request.get_json()
    if not data or not data.get('title') or not data.get('amount') or not data.get('date'):
        return jsonify(message="Invalid data. Title, amount, and date are required."), 400
    try:
        new_expense = Expense(
            title=data['title'],
            amount=data['amount'],
            category=data.get('category'),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify(new_expense.to_dict()), 201
    except (ValueError, KeyError):
        return jsonify(message="Invalid data format"), 400

@bp.route('/bulk', methods=['POST'])
@admin_required
def create_expenses_bulk():
    """Create multiple expenses in bulk."""
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify(message="Invalid data. A list of expenses is required."), 400
    
    new_expenses = []
    for item in data:
        if not item.get('title') or not item.get('amount') or not item.get('date'):
            return jsonify(message="Invalid data in list. Title, amount, and date are required for all items."), 400
        try:
            new_expense = Expense(
                title=item['title'],
                amount=item['amount'],
                category=item.get('category'),
                date=datetime.strptime(item['date'], '%Y-%m-%d').date()
            )
            new_expenses.append(new_expense)
        except (ValueError, KeyError):
            return jsonify(message="Invalid data format in list"), 400
            
    db.session.add_all(new_expenses)
    db.session.commit()
    return jsonify([expense.to_dict() for expense in new_expenses]), 201

@bp.route('', methods=['GET'])
@admin_required
def get_expenses():
    """Get all expenses."""
    expenses = Expense.query.all()
    return jsonify([expense.to_dict() for expense in expenses])

@bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_expense(id):
    """Update an existing expense."""
    expense = Expense.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify(message="Invalid data"), 400
    try:
        expense.title = data.get('title', expense.title)
        expense.amount = data.get('amount', expense.amount)
        expense.category = data.get('category', expense.category)
        if 'date' in data:
            expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        db.session.commit()
        return jsonify(expense.to_dict())
    except (ValueError, KeyError):
        return jsonify(message="Invalid data format"), 400

@bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_expense(id):
    """Delete an expense."""
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify(message="Expense deleted successfully")

@bp.route('/total', methods=['GET'])
@admin_required
def get_total_expenses():
    category = request.args.get('category')
    month = request.args.get('month')

    if not month:
        return jsonify(message="Month is required"), 400

    try:
        month_date = datetime.strptime(month, '%Y-%m').date()
    except ValueError:
        return jsonify(message="Invalid month format. Use YYYY-MM"), 400

    query = db.session.query(func.sum(Expense.amount).label('total'))
    
    if category:
        query = query.filter(Expense.category == category)
        
    query = query.filter(extract('year', Expense.date) == month_date.year,
                         extract('month', Expense.date) == month_date.month)
    
    total = query.scalar()
    
    return jsonify(total=float(total) if total else 0)

@bp.route('/total_by_category', methods=['GET'])
@admin_required
def get_total_expenses_by_category():
    month = request.args.get('month')

    if not month:
        return jsonify(message="Month is required"), 400

    try:
        month_date = datetime.strptime(month, '%Y-%m').date()
    except ValueError:
        return jsonify(message="Invalid month format. Use YYYY-MM"), 400

    results = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(
        extract('year', Expense.date) == month_date.year,
        extract('month', Expense.date) == month_date.month
    ).group_by(Expense.category).all()

    expenses_by_category = {category: float(total) for category, total in results}

    return jsonify(expenses_by_category)
