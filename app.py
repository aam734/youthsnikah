from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

DB_PATH = "database/data.db"

# HOME
@app.route('/')
def home():
    return render_template("index.html")

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = (
            request.form['full_name'],
            request.form['birth_year'],
            request.form['email'],
            request.form['phone'],
            request.form['password']
        )

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (full_name, birth_year, email, phone, password)
            VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
            SELECT * FROM users 
            WHERE (email=? OR phone=?) AND password=?
        """, (login, login, password))

        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')
        else:
            return "Invalid credentials"

    return render_template("login.html")

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (session['user_id'],))
    user = c.fetchone()
    conn.close()

    return render_template("dashboard.html", user=user)

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ACCOUNT UPDATE
@app.route('/update_account', methods=['POST'])
def update_account():
    if 'user_id' not in session:
        return redirect('/login')

    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if password:
        c.execute("""
            UPDATE users
            SET email=?, phone=?, password=?
            WHERE id=?
        """, (email, phone, password, session['user_id']))
    else:
        c.execute("""
            UPDATE users
            SET email=?, phone=?
            WHERE id=?
        """, (email, phone, session['user_id']))

    conn.commit()
    conn.close()

    return redirect('/dashboard')

import random
import string

# BIODATA
@app.route('/biodata', methods=['GET', 'POST'])
def biodata():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == 'POST':
        profile_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        data = (
            session['user_id'], profile_id,
            request.form.get('gender'),
            request.form.get('district'),
            request.form.get('current_age'),
            request.form.get('marital_status'),
            request.form.get('father_occupation'),
            request.form.get('mother_occupation'),
            request.form.get('permanent_address'),
            request.form.get('current_address'),
            request.form.get('date_of_birth'),
            request.form.get('height'),
            request.form.get('weight'),
            request.form.get('blood_group'),
            request.form.get('skin_tone'),
            request.form.get('educational_qualification'),
            request.form.get('profession'),
            request.form.get('political_view'),
            request.form.get('religion'),
            request.form.get('about_yourself'),
            request.form.get('financial_status'),
            request.form.get('social_status'),
            request.form.get('brothers'),
            request.form.get('sisters'),
            request.form.get('paternal_uncles'),
            request.form.get('maternal_uncles'),
            request.form.get('view_on_marriage'),
            request.form.get('fardh_covering'),
            request.form.get('distance_non_mahrams'),
            request.form.get('sunnah_beard'),
            request.form.get('tv_music'),
            request.form.get('can_recite_quran'),
            request.form.get('physical_mental_conditions'),
            request.form.get('prayers_five_times'),
            request.form.get('religious_work'),
            request.form.get('spouse_age'),
            request.form.get('spouse_skin_tone'),
            request.form.get('spouse_height'),
            request.form.get('spouse_weight'),
            request.form.get('spouse_education'),
            request.form.get('spouse_district'),
            request.form.get('spouse_address'),
            request.form.get('spouse_profession'),
            request.form.get('spouse_special_qualities'),
            request.form.get('guardian_marriage'),
            request.form.get('guardian_publish')
        )

        c.execute("""
            INSERT INTO biodata (
                user_id, profile_id, gender, district, current_age, marital_status,
                father_occupation, mother_occupation, permanent_address, current_address,
                date_of_birth, height, weight, blood_group, skin_tone,
                educational_qualification, profession, political_view, religion, about_yourself,
                financial_status, social_status, brothers, sisters, paternal_uncles, maternal_uncles,
                view_on_marriage, fardh_covering, distance_non_mahrams, sunnah_beard, tv_music,
                can_recite_quran, physical_mental_conditions, prayers_five_times, religious_work,
                spouse_age, spouse_skin_tone, spouse_height, spouse_weight, spouse_education,
                spouse_district, spouse_address, spouse_profession, spouse_special_qualities,
                guardian_marriage, guardian_publish
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, data)

        conn.commit()
        conn.close()
        return f"Bio Data saved successfully! (Profile ID: {profile_id})"

    return render_template("biodata.html")

if __name__ == '__main__':
    app.run(debug=True)