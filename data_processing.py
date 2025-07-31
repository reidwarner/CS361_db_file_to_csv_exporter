import sqlite3
import tempfile
import os
import csv
from _datetime import datetime


def process_sqlite_bin_helper(db_bytes):
    """
    Helper function that takes in a sql db binary file
    and makes function calls to create a csv file and
    return a tuple of the file name, db errors and csv
    errors.
    :param db_bytes: sql binary file
    :return: file_name: String
    :return: is_db_error: Boolean
    :return: is_csv_error: Boolean
    """
    # Create a temp file for processing db file
    tmp_path = create_tmp_file(db_bytes)

    # Initialize return values
    is_db_error = False
    is_csv_error = False
    file_name = ""

    try:
        # Setup database from temp file
        conn = sqlite3.connect(tmp_path)
        cursor = conn.cursor()
        # Get data from db
        table_name = get_table_name(cursor)
        headers = get_headers(cursor, table_name)
        rows = get_rows(cursor, table_name, headers)
    except:
        is_db_error = True
    finally:
        try:
            conn.close()
        except:
            pass

        # delete temp file
        os.remove(tmp_path)

    # Create CSV if there was not a db error
    if not is_db_error:
        try:
            file_name = create_csv(headers, rows)
        except:
            is_csv_error = True

    return file_name, is_db_error, is_csv_error


def create_tmp_file(db_bytes):
    """
    Create a temp file to use for processing the input db data.
    :param db_bytes: sql db binary file
    :return: tmp_path: string
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        tmp.write(db_bytes)
        tmp_path = tmp.name

    return tmp_path


def get_table_name(cursor):
    """
    Returns the name of the db table.
    :param cursor: db cursor object
    :return: string
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    return tables[0]


def get_headers(cursor, table_name):
    """
    Returns the column headers of the db table.
    :param cursor: db cursor object
    :param table_name: string
    :return: column_names: list
    """
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    column_names = [description[0] for description in cursor.description]
    return column_names[1:]


def get_rows(cursor, table_name, headers):
    """
    Returns the rows of data from the db table.
    :param cursor: db cursor object
    :param table_name: string
    :param headers: list of strings
    :return: data - list of data tuples
    """
    cols = ""
    for i in range(len(headers)):
        if i < len(headers) - 1:
            cols += f"{headers[i]}, "
        else:
            cols += f"{headers[i]}"

    cursor.execute(f"SELECT {cols} FROM {table_name}")
    data = cursor.fetchall()
    return data


def create_csv(headers, rows):
    """
    Creates a csv file in the Downloads directory and returns the
    file name.
    :param headers: list of strings
    :param rows: list of data tuples
    :return: string of file name
    """
    # Get current date and time so file naming is unique
    now = datetime.now()
    now_formatted = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"db_export_{now_formatted}.csv"

    # Get path to new file in downloads directory
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

    # Write to new csv file
    with open(downloads_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)

    return file_name
