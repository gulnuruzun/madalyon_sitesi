from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "duzce_university_secret_key"
DB_FILE = "database.db"

# -------------------------------------------------
# VERİTABANI OLUŞTURMA VE DEFAULT ADMIN
# -------------------------------------------------
def create_database_and_admin():
    # Eğer eski veritabanı varsa silelim
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Üyeler tablosu
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            student_no TEXT
        )
    ''')

    # Admin tablosu
    c.execute('''
        CREATE TABLE admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Varsayılan admin
    default_admin_user = "admin"
    default_admin_pass = "sifre123"
    pw_hash = generate_password_hash(default_admin_pass, method='pbkdf2:sha256')
    c.execute("INSERT INTO admin (username, password_hash) VALUES (?, ?)",
              (default_admin_user, pw_hash))

    conn.commit()
    conn.close()

create_database_and_admin()

# -------------------------------------------------
# SAYFALAR
# -------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sayfa2')
def sayfa2():
    return render_template('sayfa2.html')

@app.route('/sayfa3', methods=['GET', 'POST'])
def sayfa3():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        student_no = request.form.get('student_no')

        if not name or not email:
            return "Ad ve E-mail zorunludur!", 400

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, phone, student_no) VALUES (?, ?, ?, ?)",
                  (name, email, phone, student_no))
        conn.commit()
        conn.close()

        return redirect(url_for('sayfa3'))
    return render_template('sayfa3.html')

@app.route('/sayfa4')
def sayfa4():
    return render_template('sayfa4.html')

@app.route('/sayfa5')
def sayfa5():
    return render_template('sayfa5.html')

# -------------------------------------------------
# ADMIN GİRİŞ
# -------------------------------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT password_hash FROM admin WHERE username=?", (username,))
        admin = c.fetchone()
        conn.close()

        if admin and check_password_hash(admin[0], password):
            session['admin'] = username
            return redirect(url_for('admin_panel'))
        else:
            return render_template('admin_login.html', error="Hatalı kullanıcı adı veya şifre!")
    return render_template('admin_login.html')

# -------------------------------------------------
# ADMIN PANELİ (ÜYE LİSTESİ)
# -------------------------------------------------
@app.route('/admin/panel')
def admin_panel():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    return render_template('admin_panel.html', users=users)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
