from flask import Blueprint, jsonify, request
from datetime import datetime
from werkzeug.security import generate_password_hash
from utils.database import create_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if data is None:
        return jsonify({
            "message": "Request body is missing"
        }), 400
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "message": "Username, email and password are required"
        }), 400
    
    password_hash = generate_password_hash(password)

    created_at = datetime.now().isoformat()

    try:
        user = create_user(
            username,
            email,
            password_hash,
            created_at
        )

    except Exception as e:
        return jsonify({
            "message": "Username or email already exists"
        }), 409

    return jsonify({
        "message": "User registered successfully",
        "user": user
    }), 201


