from flask import Flask, jsonify, request,render_template
from routes.expenses_routes import expense_bp

app = Flask(__name__)
app.register_blueprint(expense_bp)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-expense")
def add_expense_page():
    return render_template("add_expense.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/all_expenses")
def expenses_page():
    return render_template("all_expenses.html")

if __name__ == "__main__":
    app.run(debug=True)