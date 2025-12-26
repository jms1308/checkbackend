
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

# Firestore client
db = firestore.client()

firestore_expenses_bp = Blueprint("firestore_expenses", __name__)

@firestore_expenses_bp.route("/", methods=["POST"])
def add_expense():
    """
    Adds a new expense to the "expenses" collection in Firestore.
    Expects a JSON body with "name" and "amount".
    """
    try:
        data = request.get_json()
        if not data or "name" not in data or "amount" not in data:
            return jsonify({"error": "Missing name or amount in request"}), 400

        # Add a new doc with a generated id.
        _, doc_ref = db.collection("expenses").add(data)
        
        # Return the new expense with its ID
        new_expense = doc_ref.get().to_dict()
        return jsonify({"id": doc_ref.id, **new_expense}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firestore_expenses_bp.route("/", methods=["GET"])
def get_expenses():
    """
    Retrieves all expenses from the "expenses" collection.
    """
    try:
        expenses_ref = db.collection("expenses")
        docs = expenses_ref.stream()

        expenses = []
        for doc in docs:
            expense_data = doc.to_dict()
            expense_data["id"] = doc.id
            expenses.append(expense_data)

        return jsonify(expenses), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firestore_expenses_bp.route("/<expense_id>", methods=["PUT"])
def update_expense(expense_id):
    """
    Updates an existing expense document in Firestore.
    """
    try:
        data = request.get_json()
        db.collection("expenses").document(expense_id).update(data)
        return jsonify({"success": True, "message": f"Expense {expense_id} updated."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firestore_expenses_bp.route("/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    """
    Deletes an expense document from Firestore.
    """
    try:
        db.collection("expenses").document(expense_id).delete()
        return jsonify({"success": True, "message": f"Expense {expense_id} deleted."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
