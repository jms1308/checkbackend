
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Blueprint, jsonify

# Initialize Firebase Admin SDK
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

firestore_bp = Blueprint("firestore", __name__)

@firestore_bp.route("/users", methods=["GET"])
def get_users():
    """
    Retrieves all users from the "users" collection in Firestore.
    """
    users_ref = db.collection("users")
    docs = users_ref.stream()

    users = []
    for doc in docs:
        users.append(doc.to_dict())

    return jsonify(users)
