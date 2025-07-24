# app/resources/routes.py
from flask import render_template, abort, redirect, url_for
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
    posts = get_all_blog_posts()
    return render_template('blog.html',
                         posts=posts,
                         title='Medical Billing Blog | Ardur Healthcare',
                         meta_description='Explore our medical billing blog for expert tips, coding updates, and insights to help healthcare providers simplify billing and boost reimbursement.')

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
    return redirect(url_for('resources.blog'))

# Specific blog routes with SEO data
@resources.route('/blog/what-is-medical-billing')
def what_is_medical_billing():
    """What Is Medical Billing blog post"""
    return render_template('blog_post.html',
                         post={
                             'title': 'What Is Medical Billing?',
                             'meta_title': 'What Is Medical Billing?| Ardur Healthcare',
                             'meta_description': 'Curious what is medical billing? Our complete beginner\'s guide breaks down essential processes & importance. Ardur Healthcare optimizes revenue for providers.',
                             'h1': 'what is medical billing',
                             'slug': 'what-is-medical-billing',
                             'date': datetime(2024, 1, 15),
                             'author': 'Ardur Healthcare Team',
                             'h2_sections': [
                                 'Introduction',
                                 'Medical Billing Definition: The Core Concept',
                                 'The Medical Billing Process: A Step-by-Step Walkthrough',
                                 'Importance of Medical Billing: Why It Matters',
                                 'Key Roles in Medical Billing: Who Does What?',
                                 'Types of Medical Billing: A Quick Overview',
                                 'The Future of Medical Billing & Compliance',
                                 'Conclusion',
                                 'About Ardur Healthcare'
                             ]
                         })

@resources.route('/blog/medical-coding-vs-billing')
def medical_coding_vs_billing():
    """Medical Coding vs Billing blog post"""
    return render_template('blog_post.html',
                         post={
                             'title': 'Medical Coding vs Billing: What\'s the Difference?',
                             'meta_title': 'Medical Coding vs Billing| Ardur Healthcare',
                             'meta_description': 'Understand medical coding vs billing with our guide! Learn the key differences & shared goals that drive healthcare reimbursement. Ardur Healthcare helps.',
                             'h1': 'medical coding vs billing',
                             'slug': 'medical-coding-vs-billing',
                             'date': datetime(2024, 2, 10),
                             'author': 'Ardur Healthcare Team',
                             'h2_sections': [
                                 'Understanding Medical Coding: The Language of Healthcare',
                                 'The Medical Coder: Roles and Responsibilities',
                                 'Understanding Medical Billing: The Financial Backbone',
                                 'The Medical Biller: Roles and Responsibilities',
                                 'Medical Coding vs Billing: The Key Differences (and Why They Matter)',
                                 'Collaboration for a Seamless Revenue Cycle',
                                 'Conclusion',
                                 'About Ardur Healthcare'
                             ]
                         })

@resources.route('/blog/medical-billing-denial-reasons')
def medical_billing_denial_reasons():
    """Medical Billing Denial Reasons blog post"""
    return render_template('blog_post.html',
                         post={
                             'title': 'Understanding Medical Billing Denial Reasons',
                             'meta_title': 'Medical Billing Denial Reasons| Ardur Healthcare',
                             'meta_description': 'Discover medical billing denial reasons & how to prevent them. Our guide covers common denials & strategies for effective revenue cycle management.',
                             'h1': 'medical billing denial reasons',
                             'slug': 'medical-billing-denial-reasons',
                             'date': datetime(2024, 3, 5),
                             'author': 'Ardur Healthcare Team',
                             'h2_sections': [
                                 'Introduction',
                                 'Common Medical Billing Denial Reasons',
                                 'The Cost of Denials',
                                 'How to Prevent Medical Billing Denials',
                                 'Effective Denial Management Strategies',
                                 'When to Consider Outsourced Medical Billing',
                                 'Conclusion',
                                 'About Ardur Healthcare'
                             ]
                         })

@resources.route('/blog/cpt-icd10-hcpcs-codes')
def cpt_icd10_hcpcs_codes():
    """CPT ICD-10 HCPCS Codes blog post"""
    return render_template('blog_post.html',
                         post={
                             'title': 'Understanding CPT, ICD-10, and HCPCS Codes: Medical Billing Basics',
                             'meta_title': 'Understanding CPT, ICD-10, and HCPCS Codes| Ardur Healthcare',
                             'meta_description': 'Understand CPT ICD-10 HCPCS codes with our guide! Learn their roles in medical coding, billing, & why accurate coding is vital for your practice.',
                             'h1': 'CPT ICD-10 HCPCS codes',
                             'slug': 'cpt-icd10-hcpcs-codes',
                             'date': datetime(2024, 4, 20),
                             'author': 'Ardur Healthcare Team',
                             'h2_sections': [
                                 'Introduction',
                                 'What Are CPT Codes? The Language of Procedures',
                                 'What Are ICD-10 Codes? The Language of Diagnoses',
                                 'What Are HCPCS Codes? The Language of Supplies and More',
                                 'Why These Medical Coding Systems Are So Important',
                                 'The Impact of Accurate Coding: Avoiding Costly Mistakes',
                                 'Conclusion',
                                 'About Ardur Healthcare'
                             ]
                         })

@resources.route('/blog/medical-billing-process-overview')
def medical_billing_process_overview():
    """Medical Billing Process blog post"""
    return render_template('blog_post.html',
                         post={
                             'title': 'Medical Billing Process: Step-by-Step Overview',
                             'meta_title': 'Medical Billing Process Explained| Ardur Healthcare',
                             'meta_description': 'Understand the medical billing process with our step-by-step guide! Learn the workflow from patient registration to payment. Optimize your revenue cycle.',
                             'h1': 'medical billing process',
                             'slug': 'medical-billing-process-overview',
                             'date': datetime(2024, 5, 15),
                             'author': 'Ardur Healthcare Team',
                             'h2_sections': [
                                 'Introduction',
                                 'The Starting Line: Pre-Service Steps',
                                 'Behind the Scenes: From Service to Codes',
                                 'The Core of the Process: Claim Creation & Submission',
                                 'Post-Submission: Tracking and Getting Paid',
                                 'The Final Step: Patient Billing',
                                 'Why a Smooth Medical Billing Workflow Matters',
                                 'About Ardur Healthcare'
                             ]
                         })

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
