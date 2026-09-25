from flask import Blueprint, jsonify, request 
from datetime import datetime,timedelta
from utils.dashboard import ( calculate_monthly_total,calculate_daily_average ) 
from utils.database import (create_expense,get_expenses, get_expense_by_id,
                            update_expense_in_db,delete_expense_in_db)
from utils.insight_utils import (get_current_month_range,get_highest_spending_category,get_monthly_spending_comparison,
                            get_current_month_expenses,get_small_expenses,get_spending_days) 
from data.expense_model import Expense 
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

expense_bp = Blueprint("expenses",__name__)
#Helper function
def validate_expense(data):
    try:
        return Expense(**data), None

    except ValidationError as e:
        errors = []

        for error in e.errors():
            error = error.copy()
            error.pop("ctx", None)
            error.pop("url", None)
            errors.append(error)

        return None, errors

@expense_bp.route("/expenses", methods=["POST"])
@jwt_required()
def add_expense():
    data = request.get_json()
    if data is None:
        return jsonify({
            "message": "Request body is missing"
        }), 400

    expense_data, errors = validate_expense(data)
    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    user_id = int(get_jwt_identity())
    date = datetime.now().date().isoformat()
    
    expense = create_expense(
        user_id,
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
@jwt_required()
def get_all_expenses(): 
    user_id = int(get_jwt_identity())

    category = request.args.get("category") 
    expenses = get_expenses(user_id,category) 
    return jsonify(expenses), 200 


# READ - Get one expense 
@expense_bp.route("/expenses/<int:id>", methods=["GET"]) 
@jwt_required()
def get_expense(id): 
    user_id = int(get_jwt_identity())
    expense_row = get_expense_by_id(id,user_id) 

    if expense_row: 
        return jsonify(expense_row) 
    return jsonify({ "message": "Expense not found" }),404


# UPDATE - Update an expense
@expense_bp.route("/expenses/<int:id>", methods=["PUT"])
@jwt_required()
def update_expense(id):
    data = request.get_json()

    if data is None:
        return jsonify({
            "message": "Request body is missing"
        }), 400
    
    expense_data, errors = validate_expense(data)
    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    # Check whether expense exists
    user_id = int(get_jwt_identity())
    expense = get_expense_by_id(id,user_id)

    if expense is None:
        return jsonify({
            "message": "Expense not found"
        }), 404

    date = datetime.now().date().isoformat()

    # Update database using validated Pydantic data
    update_expense_in_db(
        id,user_id,
        expense_data.amount,expense_data.category,expense_data.note,
        date,expense_data.payment_method
    )

    updated_expense = get_expense_by_id(id,user_id) # Get updated record

    return jsonify({
        "message": "Expense updated successfully",
        "expense": updated_expense
    }), 200

# DELETE - Delete an expense
@expense_bp.route("/expenses/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_expense(id):
    # Check whether expense exists
    user_id = int(get_jwt_identity())
    expense = get_expense_by_id(id,user_id)

    if expense is None:
        return jsonify({
            "message": "Expense not found"
        }), 404

    # Delete expense
    delete_expense_in_db(id,user_id)

    return jsonify({
        "message": "Expense deleted successfully"
    }), 200


#Spending_insights routes
@expense_bp.route("/expenses/insights/highest-category", methods=["GET"])
@jwt_required()
def highest_spending_category():
    user_id = int(get_jwt_identity())

    insight = get_highest_spending_category(user_id)

    if insight is None:
        return jsonify({
            "message": "No expenses found for this month"
        }), 404

    # percentage logic
    expenses = get_expenses(user_id)
    monthly_total = calculate_monthly_total(expenses)

    percentage = (insight["amount"] / monthly_total) * 100
    insight["percentage"] = round(percentage, 2)

    return jsonify(insight), 200

@expense_bp.route("/expenses/insights/daily-average", methods=["GET"])
@jwt_required()
def daily_average_spending():
    user_id = int(get_jwt_identity())
    expenses = get_expenses(user_id)

    monthly_total = calculate_monthly_total(expenses)
    daily_average = calculate_daily_average(monthly_total)

    return jsonify({
        "daily_average": daily_average
    }), 200


@expense_bp.route("/expenses/insights/monthly-compare", methods=["GET"])
@jwt_required()
def monthly_spending_comparison():
    user_id = int(get_jwt_identity())
    _, current_month_start, next_month_start = get_current_month_range()

    # First day of previous month
    previous_month_end = current_month_start - timedelta(days=1)
    previous_month_start = previous_month_end.replace(day=1)

    result = get_monthly_spending_comparison(
        user_id,
        current_month_start.isoformat(),
        next_month_start.isoformat(),
        previous_month_start.isoformat()
    )

    current_total = result["current_total"]
    previous_total = result["previous_total"]

    #Comparision calculation
    difference = current_total - previous_total

    if previous_total == 0:
        percentage_change = None
    else:
        percentage_change = (difference / previous_total) * 100

    if difference > 0:
        status = "increased"
    elif difference < 0:
        status = "decreased"
    else:
        status = "unchanged"

    return jsonify({
        "current_month": current_month_start.strftime("%B %Y"),
        "previous_month": previous_month_start.strftime("%B %Y"),
        "current_total": round(current_total, 2),
        "previous_total": round(previous_total, 2),
        "difference": round(difference, 2),
        "percentage_change": (
            round(percentage_change, 2)
            if percentage_change is not None
            else None
        ),
        "status": status
    }), 200

@expense_bp.route("/expenses/insights/weekend-pattern", methods=["GET"])
@jwt_required()
def weekend_spending():
    user_id = int(get_jwt_identity())

    _, current_month_start, next_month_start = get_current_month_range()
    # Get current month's expenses
    expenses = get_current_month_expenses(
        user_id,
        current_month_start.isoformat(),next_month_start.isoformat()
    )

    weekday_total = 0
    weekend_total = 0

    for expense in expenses:
        expense_date = datetime.strptime(expense["date"],"%Y-%m-%d").date()

        if expense_date.weekday() < 5:
            weekday_total += expense["amount"]
        else:
            weekend_total += expense["amount"]

    total = weekday_total + weekend_total

    if total == 0:
        weekday_percentage = 0
        weekend_percentage = 0
    else:
        weekday_percentage = (weekday_total / total) * 100
        weekend_percentage = (weekend_total / total) * 100

    if weekend_total > weekday_total:
        pattern = "weekend"
    elif weekday_total > weekend_total:
        pattern = "weekday"
    else:
        pattern = "equal"

    return jsonify({
        "month": current_month_start.strftime("%B %Y"),
        "weekday_total": round(weekday_total, 2),
        "weekend_total": round(weekend_total, 2),
        "weekday_percentage": round(weekday_percentage, 2),
        "weekend_percentage": round(weekend_percentage, 2),
        "pattern": pattern
    }), 200

@expense_bp.route("/expenses/insights/small-expenses", methods=["GET"])
@jwt_required()
def small_expenses():
    user_id = int(get_jwt_identity())

    _, current_month_start, next_month_start = get_current_month_range()

    data = get_small_expenses(
        user_id,
        current_month_start.isoformat(),next_month_start.isoformat()
    )

    return jsonify({
        "month": current_month_start.strftime("%B %Y"),
        "threshold": 200,
        "count": data["count"],
        "total": round(data["total"], 2)
    }), 200

@expense_bp.route("/expenses/insights/no-spend-days", methods=["GET"])
@jwt_required()
def no_spend_days():
    user_id = int(get_jwt_identity())

    today, current_month_start, next_month_start = get_current_month_range()

    spending_days = get_spending_days(
        user_id,
        current_month_start.isoformat(),next_month_start.isoformat()
    )

    days_elapsed = today.day
    no_spend_days = days_elapsed - spending_days

    return jsonify({
        "month": current_month_start.strftime("%B %Y"),
        "days_elapsed": days_elapsed,
        "spending_days": spending_days,
        "no_spend_days": no_spend_days
    }), 200
