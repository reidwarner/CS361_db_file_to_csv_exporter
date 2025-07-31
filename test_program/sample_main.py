import time
import zmq
import sqlite3
import os

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")


def create_expense_db(db_name="expenses.db", addition=False):
    expense_table = [
        (19, 55.00, "2025-07-27", "Travel"),
        (20, 21.10, "2025-07-26", "Dining"),
        (21, 46.11, "2025-07-06", "Dining"),
        (22, 32.00, "2025-06-13", "Travel")
    ]

    if addition:
        expense_table.append((23, 34.11, "2025-05-07", "Parking"))

    if os.path.exists(db_name):
        os.remove(db_name)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    # Insert the data
    cursor.executemany('''
        INSERT INTO expenses (expense_id, amount, date, category)
        VALUES (?, ?, ?, ?)
    ''', expense_table)

    # Commit and close
    conn.commit()
    conn.close()


# Run the function
create_expense_db()

# Read the SQLite file as binary
with open("expenses.db", "rb") as f:
    db_bytes = f.read()

# Send the database bytes
socket.send(db_bytes)
reply = socket.recv_string()
print(reply)
time.sleep(1)

# Run the function
create_expense_db(db_name="expenses_2.db", addition=True)

# Read the SQLite file as binary
with open("expenses_2.db", "rb") as f:
    db_bytes = f.read()

# Send the database bytes
socket.send(db_bytes)


reply = socket.recv_string()
print(reply)
time.sleep(1)


socket.send(b"[0, 1, 2]")
reply = socket.recv_string()
print(reply)
time.sleep(1)