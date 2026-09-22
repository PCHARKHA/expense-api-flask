from flask import Blueprint, jsonify, request
from datetime import datetime

from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity

from utils.database import create_user, get_user_by_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()

    return jsonify({
        "message": "You have access to this protected route",
        "user_id": user_id
    }), 200

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
        user = create_user(username,email,password_hash,created_at)

    except Exception as e:
        return jsonify({
            "message": "Username or email already exists"
        }), 409

    return jsonify({
        "message": "User registered successfully",
        "user": user
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if data is None:
        return jsonify({
            "message": "Request body is missing"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = get_user_by_email(email)

    if user is None:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    password_valid = check_password_hash(user["password_hash"],password)
    
    if not password_valid:
        return jsonify({
            "message": "Invalid email or password"
        }), 401
    
    access_token = create_access_token(identity=str(user["id"]))
    
    return jsonify({
        "message": "Login successful",
         "access_token": access_token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    }), 200

