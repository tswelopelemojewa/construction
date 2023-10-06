import sqlite3
import pickle
import os
import numpy as np
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'MpHoMabidikama@1999'


# Create SQLite capstone and table
conn = sqlite3.connect('capstonedb.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
conn.commit()
conn.close()


# Function to hash the password
def hash_password(password):
    return generate_password_hash(password)

# Function to verify hashed password
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        # role = request.form['role']
        password = request.form['password']

        # Hash the password
        hashed_password = hash_password(password)

        conn = sqlite3.connect('capstonedb.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username,  password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        return render_template('login.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('capstonedb.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and verify_password(user[2], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials. Please try again.'

    return render_template('login.html')



@app.route('/')
def home():
    username = session.get('username')
    if username:
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


# model predictions

# Import the model as pickle file
with open('Construction.pkl','rb') as capstone_model:
        model = pickle.load(capstone_model)


# Run predictions 
@app.route('/predict', methods=['POST'])
def ml_route():
    if request.method == 'POST':
        data = request.get_json()
  
        laborers = data['laborers']
        cash_flow = data['cash_flow']
        Errors = data['Errors']
        communication = data['communication']
        Change_schedule = data['Change_schedule']
        bid_price = data['bid_price']
        scope_change = data['scope_change']
        Weather_conditions = data['Weather_conditions']
        Accidents = data['Accidents']


        # Reshape features and make prediction using the loaded model
        features = np.array([[laborers, cash_flow, Errors, communication,Change_schedule, bid_price, scope_change, Weather_conditions, Accidents]])
        prediction = model.predict(features)[0]

        return jsonify({'prediction': prediction.tolist()})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run(debug=True)


