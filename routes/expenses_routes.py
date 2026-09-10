from flask import Blueprint, jsonify, request
from datetime import datetime
from utils.dashboard import (
    calculate_monthly_total,
    calculate_weekly_total,
    calculate_daily_total
)
from utils.validation import validate_data
from utils.database import (create_expense,get_expenses,
                            get_expense_by_id,update_expense_in_db,delete_expense_in_db)

expense_bp = Blueprint("expenses",__name__)

# CREATE - Add an expense
@expense_bp.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    #Check if data exists
    if data is None:
        return jsonify({
            "message": "Request body is missing"
        }), 400
    
    error = validate_data(data)
    if error:
        return jsonify({
            "message": error
        }), 400
    
    date = datetime.now().date().isoformat()
    
    expense = create_expense(
        data["amount"],
        data["category"],
        data.get("note"),
        date
    )

    return jsonify({
        "message": "Expense added successfully",
        "expense": expense
    }),201

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

    return jsonify({
        "message": "Expense not found"
    }),404


# UPDATE - Update an expense
@expense_bp.route("/expenses/<int:id>", methods=["PUT"])
def update_expense(id):
    data = request.get_json()
    if data is None:
        return jsonify({
            "message": "Request body is missing"
        }), 400

    error = validate_data(data)
    if error:
        return jsonify({
            "message": error
        }), 400
    
    expense = get_expense_by_id(id)

    if expense is None:
        return jsonify({
            "message": "Expense not found"
        }), 404

    date = datetime.now().date().isoformat()

    update_expense_in_db(
        id,
        data["amount"],
        data["category"],
        data.get("note"),
        date
    )

    updated_expense = get_expense_by_id(id)
    return jsonify({
        "message": "Expense updated successfully",
        "expense": updated_expense
            }),200

# DELETE - Delete an expense
@expense_bp.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    expense = get_expense_by_id(id)

    if expense is None:
        return jsonify({
            "message": "Expense not found"
        }), 404

    delete_expense_in_db(id)

    return jsonify({
        "message": "Expense deleted successfully"
    }), 200

@expense_bp.route("/expenses/dashboard", methods=["GET"])
def get_dashboard():
    expenses = get_expenses()

    daily_total = calculate_daily_total(expenses)
    weekly_total = calculate_weekly_total(expenses)
    monthly_total = calculate_monthly_total(expenses)

    return jsonify({
        "daily_total": daily_total,
        "weekly_total": weekly_total,
        "monthly_total": monthly_total
    }), 200
