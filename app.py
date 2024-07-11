from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database configuration
DB_NAME = 'data.db'


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            bag_model TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        bag_model = request.form['bag_model']
        
        # Store in database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO submissions (name, email, bag_model)
            VALUES (?, ?, ?)
        ''', (name, email, bag_model))
        conn.commit()
        conn.close()
        
        return redirect(url_for('thank_you'))

# Route to display submitted data
@app.route('/thank_you')
def thank_you():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions ORDER BY id DESC')
    submissions = cursor.fetchall()
    conn.close()
    return render_template('thank_you.html', submissions=submissions)

# Route to serve the main page
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
