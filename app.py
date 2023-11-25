from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


session = {}
# Function to connect to the database
def connect_db():
    return sqlite3.connect('data.db')

def create_db():
    # Create database
    conn = connect_db()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (taskID INTEGER PRIMARY KEY AUTOINCREMENT, 
                 title TEXT, 
                 description TEXT,
                 date DATETIME DEFAULT CURRENT_TIMESTAMP,
                 deadline TIME)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (userID INTEGER PRIMARY KEY AUTOINCREMENT, 
                 firstname TEXT,
                 username TEXT, 
                 password TEXT,
                 role TEXT)''')  # Add userID later
    
    c.execute('''INSERT INTO users (firstname, username, password, role)
                 VALUES ('John Doe', 'john_doe', 'password123', 'Admin')''')
    
    conn.commit()
    conn.close()


@app.route('/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        val = database.check_login(username, password)
        if val == None:
            print("Username and/or password is none")
            return redirect(url_for('loginInvalid'))
        session['name'] = val[1]['firstname']
        session['userID'] = val[0]['userID']
        session['logged_in'] = True

        if val[4] == "Admin":
            session['isAdmin'] = True
        else:
            session['isAdmin'] = False

    print(session)
    return render_template('login.html')

@app.route('/l', methods = ['POST', 'GET'])
def loginInvalid():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        val = database.check_login(username, password)
        if val == None:
            print("Username and/or password is none")
            return redirect(url_for('loginInvalid'))
        session['name'] = val[1]['firstname']
        session['userID'] = val[0]['userID']
        session['logged_in'] = True
        if val[4] == "Admin":
            session['isAdmin'] = True
        else:
            session['isAdmin'] = False

    print(session)
    return render_template('loginInvalid.html')

# Home page - Display existing posts
@app.route('/home')
def index():
    create_db()
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    print(tasks)
    connection.close()
    return render_template('index.html', tasks=tasks)

# Add post form
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Add the new post to the database
        database.create_post(title, content)

        return redirect(url_for('index'))

    return render_template('createPost.html')

@app.route('/delete')
def delete():
    create_db()
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts")

    return render_template('index.html')

if __name__ == '__main__':

    app.run(debug=True)
