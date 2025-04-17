import sqlite3

def drop_table(db_name, table_name):
    # connecting to the SQLite database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    try:
        # the SQL query to drop the table
        query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(query)
        connection.commit()
        print(f"'{table_name}' has been dropped successfully.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        # closing the cursor and connection
        cursor.close()
        connection.close()

db_name = '../database.db'

def inputTable():
    table_name = input("Enter table name to drop (enter q to quit): ")
    if (table_name.lower() == "q"):
        exit()
    drop_table(db_name, table_name)
    inputTable()

inputTable()