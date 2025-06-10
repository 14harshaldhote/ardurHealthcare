from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SignupForm, LoginForm
from .models import User
from ..utils.file_ops import read_json, write_json

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = SignupForm()
    if form.validate_on_submit():
        users = read_json(current_app.config['USERS_FILE'])
        if form.username.data in users:
            flash('Username already taken. Please choose another.', 'error')
            return render_template('signup.html', form=form)
        
        # Create new user
        users[form.username.data] = {
            'email': form.email.data,
            'password_hash': generate_password_hash(form.password.data)
        }
        write_json(current_app.config['USERS_FILE'], users)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        users = read_json(current_app.config['USERS_FILE'])
        user_data = users.get(form.username.data)
        
        if user_data and check_password_hash(user_data['password_hash'], form.password.data):
            user = User(form.username.data, user_data['email'])
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))