# app/main/routes.py
from flask import render_template, redirect, url_for
import json
import os
from . import main  # Import the blueprint created in app/main/__init__.py

def load_specialty_data():
    """Load specialty data from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'specialty', 'specialty_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('services', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/services')
def services():
    return redirect(url_for('services.index'))

@main.route('/resources')
def resources():
    return render_template('resources.html', title='Resources')
