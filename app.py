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
            WHERE email=? AND password=?
        """, (login, password))

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

def generate_profile_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=6))
    digits = ''.join(random.choices(string.digits, k=10))
    return letters + digits

# BIODATA ( FIXED )
@app.route('/biodata', methods=['GET', 'POST'])
def biodata():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Check existing biodata
    c.execute("SELECT * FROM biodata WHERE user_id=?", (session['user_id'],))
    existing = c.fetchone()

    if request.method == 'POST':
        try:
            while True:
                profile_id = generate_profile_id()
                c.execute("SELECT 1 FROM biodata WHERE profile_id=?", (profile_id,))
                if not c.fetchone():
                    break

            form = request.form

            if existing:
                # UPDATE
                c.execute("""
                UPDATE biodata SET
                    gender=?, district=?, current_age=?, marital_status=?,
                    father_occupation=?, mother_occupation=?, permanent_address=?, current_address=?,
                    date_of_birth=?, height=?, weight=?, blood_group=?, skin_tone=?,
                    educational_qualification=?, profession=?, political_view=?, religion=?, about_yourself=?,
                    financial_status=?, social_status=?, brothers=?, sisters=?, paternal_uncles=?, maternal_uncles=?,
                    view_on_marriage=?, fardh_covering=?, distance_non_mahrams=?, sunnah_beard=?, tv_music=?,
                    can_recite_quran=?, physical_mental_conditions=?, prayers_five_times=?, religious_work=?,
                    spouse_age=?, spouse_skin_tone=?, spouse_height=?, spouse_weight=?, spouse_education=?,
                    spouse_district=?, spouse_address=?, spouse_profession=?, spouse_special_qualities=?,
                    guardian_marriage=?, guardian_publish=?
                WHERE user_id=?
                """, (
                    form.get('gender'), form.get('district'), form.get('current_age'), form.get('marital_status'),
                    form.get('father_occupation'), form.get('mother_occupation'), form.get('permanent_address'), form.get('current_address'),
                    form.get('date_of_birth'), form.get('height'), form.get('weight'), form.get('blood_group'), form.get('skin_tone'),
                    form.get('educational_qualification'), form.get('profession'), form.get('political_view'), form.get('religion'), form.get('about_yourself'),
                    form.get('financial_status'), form.get('social_status'), form.get('brothers'), form.get('sisters'),
                    form.get('paternal_uncles'), form.get('maternal_uncles'),
                    form.get('view_on_marriage'), form.get('fardh_covering'), form.get('distance_non_mahrams'), form.get('sunnah_beard'),
                    form.get('tv_music'), form.get('can_recite_quran'), form.get('physical_mental_conditions'),
                    form.get('prayers_five_times'), form.get('religious_work'),
                    form.get('spouse_age'), form.get('spouse_skin_tone'), form.get('spouse_height'),
                    form.get('spouse_weight'), form.get('spouse_education'), form.get('spouse_district'),
                    form.get('spouse_address'), form.get('spouse_profession'), form.get('spouse_special_qualities'),
                    form.get('guardian_marriage'), form.get('guardian_publish'),
                    session['user_id']
                ))

            else:
                # INSERT
                c.execute("""
                INSERT INTO biodata (
                    user_id, profile_id,
                    gender, district, current_age, marital_status,
                    father_occupation, mother_occupation, permanent_address, current_address,
                    date_of_birth, height, weight, blood_group, skin_tone,
                    educational_qualification, profession, political_view, religion, about_yourself,
                    financial_status, social_status, brothers, sisters, paternal_uncles, maternal_uncles,
                    view_on_marriage, fardh_covering, distance_non_mahrams, sunnah_beard, tv_music,
                    can_recite_quran, physical_mental_conditions, prayers_five_times, religious_work,
                    spouse_age, spouse_skin_tone, spouse_height, spouse_weight, spouse_education,
                    spouse_district, spouse_address, spouse_profession, spouse_special_qualities,
                    guardian_marriage, guardian_publish
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    session['user_id'], profile_id,
                    form.get('gender'), form.get('district'), form.get('current_age'), form.get('marital_status'),
                    form.get('father_occupation'), form.get('mother_occupation'), form.get('permanent_address'), form.get('current_address'),
                    form.get('date_of_birth'), form.get('height'), form.get('weight'), form.get('blood_group'), form.get('skin_tone'),
                    form.get('educational_qualification'), form.get('profession'), form.get('political_view'), form.get('religion'), form.get('about_yourself'),
                    form.get('financial_status'), form.get('social_status'), form.get('brothers'), form.get('sisters'),
                    form.get('paternal_uncles'), form.get('maternal_uncles'),
                    form.get('view_on_marriage'), form.get('fardh_covering'), form.get('distance_non_mahrams'), form.get('sunnah_beard'),
                    form.get('tv_music'), form.get('can_recite_quran'), form.get('physical_mental_conditions'),
                    form.get('prayers_five_times'), form.get('religious_work'),
                    form.get('spouse_age'), form.get('spouse_skin_tone'), form.get('spouse_height'),
                    form.get('spouse_weight'), form.get('spouse_education'), form.get('spouse_district'),
                    form.get('spouse_address'), form.get('spouse_profession'), form.get('spouse_special_qualities'),
                    form.get('guardian_marriage'), form.get('guardian_publish')
                ))

            conn.commit()
            return redirect('/view_biodata')

        except Exception as e:
            return f"ERROR: {str(e)}"

    return render_template("biodata.html", biodata=existing)

# VIEW BIODATA
@app.route('/view_biodata')
def view_biodata():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM biodata WHERE user_id=?", (session['user_id'],))
    data = c.fetchone()

    conn.close()
    return render_template("view_biodata.html", biodata=data)

# PROFILE
@app.route('/profile/<profile_id>')
def profile(profile_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM biodata WHERE profile_id=?", (profile_id,))
    data = c.fetchone()

    conn.close()

    if not data:
        return "Profile not found"

    # Privacy check
    if data['guardian_publish'] != 'Y':
        return "This profile is private"

    return render_template("profile.html", biodata=data)

# PUBLIC PROFILE
@app.route('/public_profile')
def public_profile_list():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Only public profiles
    c.execute("SELECT profile_id, gender, district, current_age FROM biodata WHERE guardian_publish='Y'")
    profiles = c.fetchall()

    conn.close()

    return render_template("public_profile.html", profiles=profiles)

# AUTO-SAVE
@app.route('/save_biodata_step', methods=['POST'])
@login_required
def save_biodata_step():
    data = request.json
    user_id = session['user_id']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Update only fields present in the step
    for key, value in data.items():
        c.execute(f"UPDATE biodata SET {key}=? WHERE user_id=?", (value, user_id))

    conn.commit()
    conn.close()
    return '', 204

# LAST PORTION
if __name__ == '__main__':
    app.run(debug=True)
