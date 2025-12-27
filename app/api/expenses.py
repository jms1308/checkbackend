
from flask import Blueprint, request, jsonify
from app.models.expense import Expense
from app.extensions import db
from datetime import datetime

bp = Blueprint('expenses', __name__)

@bp.route('', methods=['POST'])
def add_expense():
    '''
    Add a single expense
    ---
    tags:
      - expenses
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: The title of the expense
            amount:
              type: number
              description: The amount of the expense
            category:
              type: string
              description: The category of the expense
            date:
              type: string
              format: date
              description: The date of the expense (YYYY-MM-DD)
    responses:
      201:
        description: Expense added successfully
      400:
        description: Invalid data
    '''
    data = request.get_json()
    if not data:
        return jsonify(message="Invalid data"), 400
    try:
        expense = Expense(
            title=data['title'],
            amount=data['amount'],
            category=data['category'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        db.session.add(expense)
        db.session.commit()
        return jsonify(expense.to_dict()), 201
    except (ValueError, KeyError) as e:
        return jsonify(message=f"Invalid data for item: {data}. Error: {e}"), 400

@bp.route('/bulk', methods=['POST'])
def add_expenses_bulk():
    '''
    Add multiple expenses in a single request
    ---
    tags:
      - expenses
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
                description: The title of the expense
              amount:
                type: number
                description: The amount of the expense
              category:
                type: string
                description: The category of the expense
              date:
                type: string
                format: date
                description: The date of the expense (YYYY-MM-DD)
    responses:
      201:
        description: Expenses added successfully
      400:
        description: Invalid data
    '''
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify(message="Invalid data: expected a list of expenses"), 400

    new_expenses = []
    errors = []
    for item in data:
        try:
            expense = Expense(
                title=item['title'],
                amount=item['amount'],
                category=item['category'],
                date=datetime.strptime(item['date'], '%Y-%m-%d').date()
            )
            new_expenses.append(expense)
        except (ValueError, KeyError) as e:
            errors.append(f"Invalid data for item: {item}. Error: {e}")

    if errors:
        return jsonify(message="Invalid data in bulk request", errors=errors), 400

    db.session.add_all(new_expenses)
    db.session.commit()
    return jsonify([expense.to_dict() for expense in new_expenses]), 201

@bp.route('', methods=['GET'])
def get_expenses():
    '''
    Get all expenses
    ---
    tags:
      - expenses
    responses:
      200:
        description: A list of expenses
    '''
    expenses = Expense.query.all()
    return jsonify([expense.to_dict() for expense in expenses])

@bp.route('/<int:id>', methods=['GET'])
def get_expense(id):
    '''
    Get a single expense by ID
    ---
    tags:
      - expenses
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the expense to retrieve
    responses:
      200:
        description: The expense with the specified ID
      404:
        description: Expense not found
    '''
    expense = Expense.query.get_or_404(id)
    return jsonify(expense.to_dict())

@bp.route('/<int:id>', methods=['PUT'])
def update_expense(id):
    '''
    Update an existing expense
    ---
    tags:
      - expenses
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the expense to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: The new title of the expense
            amount:
              type: number
              description: The new amount of the expense
            category:
              type: string
              description: The new category of the expense
            date:
              type: string
              format: date
              description: The new date of the expense (YYYY-MM-DD)
    responses:
      200:
        description: Expense updated successfully
      400:
        description: Invalid data format
      404:
        description: Expense not found
    '''
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
def delete_expense(id):
    '''
    Delete an expense
    ---
    tags:
      - expenses
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the expense to delete
    responses:
      200:
        description: Expense deleted successfully
      404:
        description: Expense not found
    '''
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify(message="Expense deleted successfully")
