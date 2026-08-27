from flask import Flask, jsonify, request
app = Flask(__name__)

# Temporary in-memory data
expenses_data = [
    {
        "id": 1,
        "title": "Lunch",
        "amount": 250,
        "category": "Food"
    },
    {
        "id": 2,
        "title": "Bus",
        "amount": 50,
        "category": "Travel"
    }
]

# HOME
@app.route("/")
def home():
    return "Expense API is running"


# CREATE - Add an expense
@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()

    new_id = len(expenses_data) + 1
    expense = {
        "id": new_id,
        "title": data["title"],
        "amount": data["amount"],
        "category": data["category"]
    }

    expenses_data.append(expense)

    return jsonify({
        "message": "Expense added successfully",
        "expense": expense
    })

# READ - Get all expenses
@app.route("/expenses", methods=["GET"])
def get_expenses():

    return jsonify(expenses_data)


# READ - Get one expense
@app.route("/expenses/<int:id>", methods=["GET"])
def get_expense(id):
    for expense in expenses_data:
        if expense["id"] == id:
            return jsonify(expense)

    return jsonify({
        "message": "Expense not found"
    })


# UPDATE - Update an expense
@app.route("/expenses/<int:id>", methods=["PUT"])
def update_expense(id):
    data = request.get_json()
    for expense in expenses_data:
        if expense["id"] == id:

            expense["title"] = data["title"]
            expense["amount"] = data["amount"]
            expense["category"] = data["category"]

            return jsonify({
                "message": "Expense updated successfully",
                "expense": expense
            })

    return jsonify({
        "message": "Expense not found"
    })


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
    })

if __name__ == "__main__":
    app.run(debug=True)