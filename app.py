from flask import Flask, render_template, request
import sqlite3 as sql
import hashlib

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

@app.route('/')
def hello_world():
    return render_template('index.html')

# ============== User Auth ============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        check = check_login(username, password)

        if check:
            categories = get_top_level_categories()
            return render_template('home.html', user=username, categories=categories)
        else:
            return render_template('userLogin.html', error="Invalid credentials. Try again.")

    return render_template('userLogin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        check = insertUser(username, password)

        if check:
            categories = get_top_level_categories()
            return render_template('home.html', user=username, categories=categories)
        else:
            return render_template('userSignUp.html', error="User Exists. Try logging in.")

    return render_template('userSignUp.html')

# Generating the hashed password
def generateHash(string):
    sha256 = hashlib.sha256()
    sha256.update(string.encode('utf-8'))
    return sha256.hexdigest()

# Adding new user to the database
def insertUser(username, password):
    connection = sql.connect("database.db")
    cursor = connection.cursor()

    # Checking if user exists already
    query = "SELECT * FROM users WHERE userID=?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    # If user does not already exist, then we add the user
    if result is None:
        query = "INSERT INTO users (userID, password) VALUES (?, ?)"
        cursor.execute(query, (username, generateHash(password)))
        connection.commit()
        connection.close()
        return True

    # If user exists, we return False for error handling
    return False

# Checking user login info
def check_login(userID, password):
    connection = sql.connect("database.db")
    cursor = connection.cursor()

    query = "SELECT * FROM Users WHERE userID=?"
    cursor.execute(query, (userID,))

    result = cursor.fetchone()  # fetching the user

    connection.close()  # closing the connection

    # If user doesn't exist, we return false
    if result is None:
        return False
    # If user does exist, we compare password hashes
    else:
        hashed_pass = generateHash(password)
        if result[1] == hashed_pass:
            return True
        else:
            return False

# ===========================================================

# ============== Category Hierarchy ============================
def get_db_connection():
    connection = sql.connect('database.db')
    connection.row_factory = sql.Row
    return connection

# Get top-level categories
def get_top_level_categories():
    conn = get_db_connection()
    # ordering in alphabetical order
    categories = conn.execute("SELECT * FROM categories WHERE parent_id IS NULL ORDER BY name").fetchall()
    conn.close()
    return categories

# Get subcategories based on parent_id
def get_subcategories(connection, parent_id=None):
    if parent_id is None:
        query = 'SELECT * FROM categories WHERE parent_id IS NULL'
        result = connection.execute(query).fetchall()
    else:
        query = 'SELECT * FROM categories WHERE parent_id = ?'
        result = connection.execute(query, (parent_id,)).fetchall()

    output = []
    for row in result:
        output.append({
            'id': row['id'],
            'name': row['name'],
            'children': get_subcategories(connection, row['id'])
        })
    return output

@app.route("/home")
def show_categories():
    conn = get_db_connection()
    categories = get_top_level_categories()  # Pre-load top-level categories
    conn.close()
    return render_template("home.html", categories=categories)

if __name__ == '__main__':
    app.run()
