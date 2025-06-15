from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets





app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Créer la table users si elle n'existe pas
def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
init_db()

# Route page d'accueil
@app.route('/home')
def home():
    return render_template('home.html')


# Page inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        with sqlite3.connect('users.db') as conn:
            try:
                conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return "Email already registered."
    return render_template('signup.html')

# Page connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('users.db') as conn:
            cur = conn.execute("SELECT password FROM users WHERE email = ?", (email,))
            user = cur.fetchone()

            if user and check_password_hash(user[0], password):
                session['user'] = email
                return redirect(url_for('home'))
            else:
                return "Invalid credentials."
    return render_template('login.html')

# Déconnexion
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/courses/module1')
def module1():
    return render_template('module1.html')



if __name__ == '__main__':
    import os
    print("Current working directory:", os.getcwd())
    print("Files in templates:", os.listdir('templates'))

    app.run(debug=True)
