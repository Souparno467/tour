from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import get_db
from forms import RegisterForm, LoginForm  # Correct import

auth_bp = Blueprint('auth', __name__)

# Register Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        db = get_db()
        try:
            db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, password))
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception:
            flash('User already exists or an error occurred.', 'danger')

    return render_template('register.html', form=form)

# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'], user['email'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html', form=form)

# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
