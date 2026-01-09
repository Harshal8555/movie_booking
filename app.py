from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="movie_booking"
)
cursor = db.cursor(dictionary=True)

# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s AND role=%s",
            (email, password, role)
        )
        user = cursor.fetchone()

        if user:
            session['user'] = user['name']
            session['role'] = user['role']
            return redirect('/admin_home' if role == 'admin' else '/user_home')
        else:
            return "Invalid Login"

    return render_template('login.html')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s)",
            (
                request.form['name'],
                request.form['email'],
                request.form['password'],
                request.form['role']
            )
        )
        db.commit()
        return redirect('/')
    return render_template('register.html')


# USER HOME
@app.route('/user_home')
def user_home():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return render_template('user_home.html', movies=movies)


# ADMIN HOME
@app.route('/admin_home')
def admin_home():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return render_template('admin_home.html', movies=movies)


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
