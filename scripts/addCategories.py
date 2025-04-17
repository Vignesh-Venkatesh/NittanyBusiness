import csv
import sqlite3

def load_categories_from_csv(csv_path, db_path):
    # connecting to the SQLite DB
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # creating the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES Categories(id)
        );
    """)

    # reading CSV
    with open(csv_path,newline='',encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # inserting parent categories first
    parent_id_map = {}
    for row in data:
        parent = row['parent_category']
        if parent not in parent_id_map:
            cursor.execute("INSERT INTO Categories (name, parent_id) VALUES (?, NULL)", (parent,))
            parent_id_map[parent] = cursor.lastrowid

    # inserting subcategories
    for row in data:
        child = row['category_name']
        parent_id = parent_id_map[row['parent_category']]
        cursor.execute("INSERT INTO Categories (name, parent_id) VALUES (?, ?)", (child, parent_id))

    connection.commit()
    connection.close()
    print("Categories successfully loaded.")

# Example usage:
load_categories_from_csv('NittanyBusinessDataset/Categories.csv', '../database.db')
