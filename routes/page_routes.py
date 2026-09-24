from flask import Blueprint, render_template

page_bp = Blueprint("pages", __name__)
@page_bp.route("/")
def home():
    return render_template("index.html")


@page_bp.route("/add-expense")
def add_expense_page():
    return render_template("add_expense.html")


@page_bp.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@page_bp.route("/all_expenses")
def expenses_page():
    return render_template("all_expenses.html")

@page_bp.route("/login")
def login_page():
    return render_template("login.html")


@page_bp.route("/register")
def register_page():
    return render_template("register.html")

@page_bp.route("/spending-insights")
def spending_insights_page():
    return render_template("spending_insights.html")