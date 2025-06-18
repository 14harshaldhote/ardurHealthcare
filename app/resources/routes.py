# app/resources/routes.py
from flask import render_template
from . import resources

@resources.route('/best_billing')
def best_billing():
    return render_template('best_billing.html')

@resources.route('/article')
def article():
    return render_template('article.html')

@resources.route('/press')
def press():
    return render_template('press.html')

@resources.route('/case')
def case():
    return render_template('case.html')

@resources.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')