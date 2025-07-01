from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create the database and user table if it doesn't exist
def init_db():
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
        # Add a default user
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'admin'))
        conn.commit()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = c.fetchone()
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid Credentials"

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
