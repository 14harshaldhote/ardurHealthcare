# app/resources/routes.py
from flask import render_template, abort
from . import resources
from .blog_data import get_all_blog_posts, get_blog_post, get_related_posts

@resources.route('/best_billing')
def best_billing():
    return render_template('best_billing.html')

@resources.route('/blog')
def blog():
    """Blog listing page with all blog posts in cards"""
    posts = get_all_blog_posts()
    return render_template('blog.html', posts=posts)

@resources.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    post = get_blog_post(slug)
    if not post:
        abort(404)

    related_posts = get_related_posts(slug, limit=3)
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@resources.route('/article')
def article():
    """Redirect old article route to new blog route"""
    return render_template('blog.html', posts=get_all_blog_posts())

@resources.route('/press')
def press():
    return render_template('press.html')

@resources.route('/case')
def case():
    return render_template('case.html')

@resources.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')
