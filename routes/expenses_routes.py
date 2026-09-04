from flask import Blueprint, jsonify, request
from datetime import datetime
from app import app

from utils.validation import validate_data
from data.expenses import expenses_data

# CREATE - Add an expense
@app.route("/expenses", methods=["POST"])
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
    
    #Creating an expense object
    expense = {}
    new_id = max([expense["id"] for expense in expenses_data], default=0) + 1
    expense["id"]= new_id
    expense["amount"]= data["amount"]
    expense["category"]=data["category"]
    expense["note"] = data.get("note") #optional
    expense["date"] = datetime.now().date().isoformat()
    
    #appending data to to main data(for now)
    expenses_data.append(expense)

    return jsonify({
        "message": "Expense added successfully",
        "expense": expense
    }),201

# READ - Get all expenses
@app.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses_data),200


# READ - Get one expense
@app.route("/expenses/<int:id>", methods=["GET"])
def get_expense(id):
    for expense in expenses_data:
        if expense["id"] == id:
            return jsonify(expense)

    return jsonify({
        "message": "Expense not found"
    }),404


# UPDATE - Update an expense
@app.route("/expenses/<int:id>", methods=["PUT"])
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
    
    for expense in expenses_data:
        if expense["id"] == id:
            expense["amount"] = data["amount"]
            expense["category"] = data["category"]
            expense["note"] = data.get("note") #optional
            expense["date"] = datetime.now().isoformat()

            return jsonify({
                "message": "Expense updated successfully",
                "expense": expense
            }),200

    return jsonify({
        "message": "Expense not found"
    }),404


# DELETE - Delete an expense
@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    for expense in expenses_data:
        if expense["id"] == id:
            expenses_data.remove(expense)

            return jsonify({
                "message": "Expense deleted successfully"
            })

    return jsonify({
        "message": "Expense not found"
    }),404
