import hashlib
import csv
import sqlite3 as sql

# Generating the hashed password
def generateHash(string):
    sha256 = hashlib.sha256()
    sha256.update(string.encode('utf-8'))
    return sha256.hexdigest()

# Initializing the database
def initializeDB():
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    # Create Users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            userID TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()
    print("Users table initialized.")

# Adding data to the database
def addDataToDatabase(userID, hashedPassword):
    connection = sql.connect('../database.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO Users (userID, password) VALUES (?, ?)", (userID, hashedPassword))
        connection.commit()
        print(f"User {userID} added successfully.")
    except sql.IntegrityError:
        print(f"User {userID} already exists.")

    connection.close()


# Initialize database and create Users table
initializeDB()



file = "./NittanyBusinessDataset/Users.csv" # file

with open(file, "r") as csvfile:
    # opening the csv file and getting data
    csvreader = csv.reader(csvfile, delimiter=',')
    rows = list(csvreader)
    data = rows[1:]  # skipping header

    # adding the row to the database
    for row in data:
        userID, password = row[0], row[1]
        hashedPassword = generateHash(password)
        addDataToDatabase(userID, hashedPassword)
