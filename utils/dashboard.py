from data.expenses import expenses_data
from datetime import datetime, timedelta

def calculate_daily_total(expenses):
    today = datetime.now().date()
    daily_total = 0
    for expense in expenses:
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d").date()
        if(today == expense_date):
            total += expense["amount"]
       
    return daily_total


def calculate_weekly_total(expenses):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    weekly_total = 0
    
    for expense in expenses:
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d").date()

        if start_of_week <= expense_date <= today:
            weekly_total += expense["amount"]

    return weekly_total

def calculate_monthly_total(expenses):
    today = datetime.now().date()
    monthly_total = 0

    for expense in expenses:
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d").date()
        if (
            expense_date.month == today.month
            and expense_date.year == today.year
        ):
            total += expense["amount"]

    return total