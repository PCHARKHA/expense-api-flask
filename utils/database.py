import sqlite3

DATABASE = "instance/expenses.db"

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        note TEXT,
        date TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    connection.commit()
    connection.close()

def create_user(username,email,password_hash,created_at):
    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO users (username, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
    """, (username, email, password_hash, created_at))

    user_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": user_id,
        "username": username,
        "email": email,
        "created_at": created_at
    }

def create_expense(user_id,amount, category, note, date,payment_method):
    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO expenses (user_id,amount, category, note, date,payment_method)
        VALUES (?, ?, ?, ?,?,?) """, (user_id,amount,category,note,date,payment_method)
    )
    expense_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return {
        "expense_id": expense_id,
        "user_id": user_id,
        "amount": amount,
        "category": category,
        "note": note,
        "date": date,
        "payment_method" : payment_method
    }

def get_expenses(user_id,category=None):
    connection = get_db_connection()

    if category:
        cursor = connection.execute("""
            SELECT * FROM expenses
            WHERE user_id = ? AND category = ?
        """, (user_id,category,))
    else:
        cursor = connection.execute("""
            SELECT * FROM expenses
            WHERE user_id = ?
        """,(user_id,))

    expenses = [dict(row) for row in cursor]
    connection.close()
    return expenses

def get_expense_by_id(expense_id,user_id):
    connection = get_db_connection()

    cursor = connection.execute("""
        SELECT * FROM expenses
        WHERE expense_id = ? AND user_id = ?
    """, (expense_id,user_id))

    row = cursor.fetchone()
    connection.close()

    if row:
        return dict(row)

    return None

def update_expense_in_db(expense_id,user_id, amount, category, note, date,payment_method):
    connection = get_db_connection()

    connection.execute("""
        UPDATE expenses
        SET amount = ?, category = ?, note = ?, date = ?, payment_method = ?
        WHERE expense_id = ? AND user_id = ?
    """, ( amount,category,note,date,payment_method,expense_id,user_id))

    connection.commit()
    connection.close()

def delete_expense_in_db(expense_id,user_id):
    connection = get_db_connection()

    cursor = connection.execute("""
        DELETE FROM expenses
        WHERE expense_id = ? AND user_id = ?
    """, (expense_id,user_id))

    connection.commit()

    deleted = cursor.rowcount

    connection.close()
    return deleted


def get_user_by_email(email):
    connection = get_db_connection()

    cursor = connection.execute("""
        SELECT * FROM users
        WHERE email = ?
    """, (email,))

    row = cursor.fetchone()
    connection.close()

    if row:
        return dict(row)

    return None


#DASHBOARD FUNCTIONS
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


    
