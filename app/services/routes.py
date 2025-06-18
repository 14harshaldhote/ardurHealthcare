# app/services/routes.py
from flask import render_template
from . import services

@services.route('/enrollment')
def enrollment():
    return render_template('enrollment.html')

@services.route('/verification')
def verification():
    return render_template('verification.html')

@services.route('/billing')
def billing():
    return render_template('billing.html')

@services.route('/accounts_receivable')
def accounts_receivable():
    return render_template('accounts_receivable.html')

@services.route('/denial_management')
def denial_management():
    return render_template('denial_management.html')

@services.route('/payment_posting')
def payment_posting():
    return render_template('payment_posting.html')