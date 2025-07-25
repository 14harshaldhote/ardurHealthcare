# app/resources/routes.py
from flask import render_template, abort, redirect, url_for, current_app
from datetime import datetime
from . import resources
from .blog_data import get_all_blog_posts, get_blog_post, get_related_posts

@resources.route('/')
def resources_index():
    """Main resources page - accessible at /resources/"""
    return render_template('resources.html',
                         title='Resources | Ardur Healthcare',
                         meta_description='Explore Ardur Healthcare\'s comprehensive resource center including medical billing blog, case studies, FAQs, and industry insights to help optimize your practice.')

@resources.route('/best_billing')
def best_billing():
    return render_template('best_billing.html')

@resources.route('/blog')
def blog():
    """Blog listing page with all blog posts in cards"""
    try:
        posts = get_all_blog_posts()
        return render_template('blog.html',
                             posts=posts,
                             title='Medical Billing Blog | Ardur Healthcare',
                             meta_description='Explore our medical billing blog for expert tips, coding updates, and insights to help healthcare providers simplify billing and boost reimbursement.')
    except Exception as e:
        # Log the error and return a fallback page
        current_app.logger.error(f"Error loading blog page: {str(e)}")
        return render_template('errors/500.html',
                             message="We're having trouble loading the blog. Please try again later."), 500

@resources.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    try:
        post = get_blog_post(slug)
        if not post:
            abort(404)

        related_posts = get_related_posts(slug, limit=3)
        return render_template('blog_post.html', post=post, related_posts=related_posts)
    except Exception as e:
        # Log the error and return a fallback page
        current_app.logger.error(f"Error loading blog post '{slug}': {str(e)}")
        return render_template('errors/500.html',
                             message="We're having trouble loading this blog post. Please try again later."), 500

@resources.route('/article')
def article():
    """Redirect old article route to new blog route"""
    return redirect(url_for('resources.blog'))

# Specific blog routes with SEO data
@resources.route('/blog/what-is-medical-billing')
def what_is_medical_billing():
    """What Is Medical Billing blog post"""
    post = get_blog_post('what-is-medical-billing')
    if not post:
        abort(404)
    related_posts = get_related_posts('what-is-medical-billing', limit=3)
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@resources.route('/blog/medical-coding-vs-billing')
def medical_coding_vs_billing():
    """Medical Coding vs Billing blog post"""
    post = get_blog_post('medical-coding-vs-billing')
    if not post:
        abort(404)
    related_posts = get_related_posts('medical-coding-vs-billing', limit=3)
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@resources.route('/blog/medical-billing-denial-reasons')
def medical_billing_denial_reasons():
    """Medical Billing Denial Reasons blog post"""
    post = get_blog_post('medical-billing-denial-reasons')
    if not post:
        abort(404)
    related_posts = get_related_posts('medical-billing-denial-reasons', limit=3)
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@resources.route('/blog/cpt-icd10-hcpcs-codes')
def cpt_icd10_hcpcs_codes():
    """CPT ICD-10 HCPCS Codes blog post"""
    post = get_blog_post('cpt-icd10-hcpcs-codes')
    if not post:
        abort(404)
    related_posts = get_related_posts('cpt-icd10-hcpcs-codes', limit=3)
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@resources.route('/blog/medical-billing-process-overview')
def medical_billing_process_overview():
    """Medical Billing Process blog post"""
    post = get_blog_post('medical-billing-process-overview')
    if not post:
        abort(404)
    related_posts = get_related_posts('medical-billing-process-overview', limit=3)
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@resources.route('/case-studies/')
def case_studies():
    """Case Studies page"""
    return render_template('case.html',
                         title='Medical Billing Case Studies | Ardur Healthcare',
                         meta_description='Explore real medical billing case studies showing how we helped providers reduce denials, increase collections, and streamline their billing operations.')

@resources.route('/case-studies')
def case_studies_no_slash():
    """Case Studies page without trailing slash"""
    return render_template('case.html',
                         title='Medical Billing Case Studies | Ardur Healthcare',
                         meta_description='Explore real medical billing case studies showing how we helped providers reduce denials, increase collections, and streamline their billing operations.')

@resources.route('/faqs/')
def faqs():
    """FAQs page"""
    return render_template('faqs.html',
                         title='Medical Billing FAQs | Ardur Healthcare',
                         meta_description='Find answers to common questions about medical billing, coding, credentialing, AR, compliance, and more. Explore our expert medical billing FAQs.',
                         h1='Medical Billing FAQs',
                         h2_sections=[
                             'General Medical Billing',
                             'Medical Billing Services We Offer',
                             'Specialty-Specific Billing',
                             'Credentialing and Enrollment',
                             'Claims, Denials & AR',
                             'Compliance, Privacy & Security',
                             'Pricing & Getting Started'
                         ])

@resources.route('/faqs')
def faqs_no_slash():
    """FAQs page without trailing slash"""
    return render_template('faqs.html',
                         title='Medical Billing FAQs | Ardur Healthcare',
                         meta_description='Find answers to common questions about medical billing, coding, credentialing, AR, compliance, and more. Explore our expert medical billing FAQs.',
                         h1='Medical Billing FAQs',
                         h2_sections=[
                             'General Medical Billing',
                             'Medical Billing Services We Offer',
                             'Specialty-Specific Billing',
                             'Credentialing and Enrollment',
                             'Claims, Denials & AR',
                             'Compliance, Privacy & Security',
                             'Pricing & Getting Started'
                         ])

@resources.route('/press')
def press():
    return render_template('press.html')

@resources.route('/case')
def case():
    return redirect(url_for('resources.case_studies'))

@resources.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')
