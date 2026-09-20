from flask import Blueprint, jsonify, request 
from datetime import datetime 
from utils.dashboard import ( calculate_monthly_total, calculate_weekly_total, calculate_daily_total ) 
from utils.database import (create_expense,get_expenses, get_expense_by_id,update_expense_in_db,delete_expense_in_db) 
from data.expense_model import Expense 
from pydantic import ValidationError

expense_bp = Blueprint("expenses",__name__)

@expense_bp.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()

    if data is None:
        return jsonify({
            "message": "Request body is missing"
        }), 400

    try:
        expense_data = Expense(**data)

    except ValidationError as e:
        print("PYDANTIC ERROR:", e)
        print("ERRORS:", e.errors())

        errors = []

        for error in e.errors():
            error = error.copy()
            error.pop("ctx", None)
            error.pop("url", None)
            errors.append(error)

        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    date = datetime.now().date().isoformat()

    expense = create_expense(
        expense_data.amount,
        expense_data.category,
        expense_data.note,
        date,
        expense_data.payment_method
    )

    return jsonify({
        "message": "Expense added successfully",
        "expense": expense
    }), 201

# READ - Get all expenses 
@expense_bp.route("/expenses", methods=["GET"]) 
def get_all_expenses(): 
    category = request.args.get("category") 
    expenses = get_expenses(category) 
    return jsonify(expenses), 200 


# READ - Get one expense 
@expense_bp.route("/expenses/<int:id>", methods=["GET"]) 
def get_expense(id): 
    expense_row = get_expense_by_id(id) 
    if expense_row: 
        return jsonify(expense_row) 
    return jsonify({ "message": "Expense not found" }),404


# UPDATE - Update an expense
@expense_bp.route("/expenses/<int:id>", methods=["PUT"])
def update_expense(id):
    data = request.get_json()

    if data is None:
        return jsonify({
            "message": "Request body is missing"
        }), 400

    # Validate request using Pydantic
    try:
        expense_data = Expense(**data)

    except ValidationError as e:
        print("PYDANTIC ERROR:", e)
        print("ERRORS:", e.errors()) #e.errors gives dictionary of errors

        errors = []

        for error in e.errors():
            error = error.copy()
            # Cleaning unnecessary internal information
            # & then return to API JSON's response
            error.pop("ctx", None)
            error.pop("url", None)
            errors.append(error)

        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    # Check whether expense exists
    expense = get_expense_by_id(id)

    if expense is None:
        return jsonify({
            "message": "Expense not found"
        }), 404

    date = datetime.now().date().isoformat()

    # Update database using validated Pydantic data
    update_expense_in_db(
        id,
        expense_data.amount,
        expense_data.category,
        expense_data.note,
        date,
        expense_data.payment_method
    )

    # Get updated record
    updated_expense = get_expense_by_id(id)

    return jsonify({
        "message": "Expense updated successfully",
        "expense": updated_expense
    }), 200

# DELETE - Delete an expense
@expense_bp.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    # Check whether expense exists
    expense = get_expense_by_id(id)

    if expense is None:
        return jsonify({
            "message": "Expense not found"
        }), 404

    # Delete expense
    delete_expense_in_db(id)

    return jsonify({
        "message": "Expense deleted successfully"
    }), 200
