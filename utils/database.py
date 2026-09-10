import sqlite3

DATABASE = "instance/expenses.db"

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def create_expense(amount, category, note, date):
    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO expenses (amount, category, note, date)
        VALUES (?, ?, ?, ?)
    """, (
        amount,
        category,
        note,
        date
    ))
    expense_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return {
        "id": expense_id,
        "amount": amount,
        "category": category,
        "note": note,
        "date": date
    }

def get_expenses(category=None):
    connection = get_db_connection()

    if category:
        cursor = connection.execute("""
            SELECT * FROM expenses
            WHERE category = ?
        """, (category,))
    else:
        cursor = connection.execute("""
            SELECT * FROM expenses
        """)

    expenses = [dict(row) for row in cursor]
    connection.close()
    return expenses

def get_expense_by_id(expense_id):
    connection = get_db_connection()

    cursor = connection.execute("""
        SELECT * FROM expenses
        WHERE id = ?
    """, (expense_id,))

    row = cursor.fetchone()
    connection.close()

    if row:
        return dict(row)

    return None

def update_expense_in_db(expense_id, amount, category, note, date):
    connection = get_db_connection()

    connection.execute("""
        UPDATE expenses
        SET amount = ?, category = ?, note = ?, date = ?
        WHERE id = ?
    """, (
        amount,
        category,
        note,
        date,
        expense_id
    ))

    connection.commit()
    connection.close()

def delete_expense_in_db(expense_id):
    connection = get_db_connection()

    cursor = connection.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()

    deleted = cursor.rowcount

    connection.close()
    return deleted

    
