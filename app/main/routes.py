# app/main/routes.py
from flask import render_template
from . import main  # Import the blueprint created in app/main/__init__.py

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/services')
def services():
    return render_template('services.html', title='Services')

@main.route('/resources')
def resources():
    return render_template('resources.html', title='Resources')


@main.route('/specialities')
def specialities():
    return render_template('specialities.html', title='Specialities')