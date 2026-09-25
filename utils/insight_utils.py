from datetime import datetime
from utils.database import get_db_connection
def get_current_month_range():
    today = datetime.now().date()
    current_month_start = today.replace(day=1)

    if current_month_start.month == 12:
        next_month_start = current_month_start.replace(
            year=current_month_start.year + 1,
            month=1
        )
    else:
        next_month_start = current_month_start.replace(
            month=current_month_start.month + 1
        )

    return today, current_month_start, next_month_start

def get_highest_spending_category(user_id):
    connection = get_db_connection()

    cursor = connection.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
          AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """, (user_id,))

    row = cursor.fetchone()
    connection.close()

    if row:
        return {
            "category": row["category"],
            "amount": row["total"]
        }

    return None

def get_monthly_spending_comparison(user_id, current_month_start, next_month_start, previous_month_start):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Current month total
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND date >= ?
        AND date < ?
    """, (user_id, current_month_start, next_month_start))

    current_total = cursor.fetchone()[0]

    # Previous month total
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND date >= ?
        AND date < ?
    """, (user_id, previous_month_start, current_month_start))

    previous_total = cursor.fetchone()[0]

    conn.close()

    return {
        "current_total": current_total,
        "previous_total": previous_total
    }

def get_current_month_expenses(user_id, current_month_start, next_month_start):
    connection = get_db_connection()

    cursor = connection.execute("""
        SELECT amount, category, date
        FROM expenses
        WHERE user_id = ?
        AND date >= ?
        AND date < ?
    """, (user_id, current_month_start, next_month_start))

    expenses = [dict(row) for row in cursor]

    connection.close()
    return expenses


def get_small_expenses(user_id, current_month_start, next_month_start):
    connection = get_db_connection()

    cursor = connection.execute("""
        SELECT COUNT(*) AS count, COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE user_id = ?
        AND date >= ?
        AND date < ?
        AND amount < 200
    """, (user_id, current_month_start, next_month_start))

    row = cursor.fetchone()

    connection.close()

    return {
        "count": row["count"],
        "total": row["total"]
    }

def get_spending_days(user_id, current_month_start, next_month_start):
    connection = get_db_connection()
    cursor = connection.execute("""
        SELECT COUNT(DISTINCT date) AS spending_days
        FROM expenses
        WHERE user_id = ?
        AND date >= ?
        AND date < ?
    """, (user_id, current_month_start, next_month_start))

    row = cursor.fetchone()
    connection.close()
    return row["spending_days"]
