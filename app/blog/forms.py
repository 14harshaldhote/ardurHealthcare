from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, URL
from wtforms.widgets import TextArea
from .models import BlogStatus, BlogCategory

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)], 
                       render_kw={'placeholder': 'Enter blog post title'})
    
    slug = StringField('URL Slug', validators=[Optional(), Length(max=200)], 
                      render_kw={'placeholder': 'auto-generated-from-title'})
    
    excerpt = TextAreaField('Excerpt', validators=[Optional(), Length(max=500)],
                           render_kw={'rows': 3, 'placeholder': 'Brief description of the blog post'})
    
    content = TextAreaField('Content', validators=[DataRequired()],
                           render_kw={'rows': 20, 'class': 'rich-text-editor'})
    
    meta_description = TextAreaField('Meta Description (SEO)', validators=[Optional(), Length(max=160)],
                                   render_kw={'rows': 2, 'placeholder': 'SEO meta description (160 characters max)'})
    
    seo_title = StringField('SEO Title', validators=[Optional(), Length(max=60)],
                           render_kw={'placeholder': 'SEO optimized title (60 characters max)'})
    
    keywords = StringField('Keywords', validators=[Optional()],
                          render_kw={'placeholder': 'medical billing, healthcare, revenue cycle (comma-separated)'})
    
    tags = StringField('Tags', validators=[Optional()],
                      render_kw={'placeholder': 'tips, guide, healthcare (comma-separated)'})
    
    category = SelectField('Category', choices=[
        (BlogCategory.MEDICAL_BILLING.value, 'Medical Billing'),
        (BlogCategory.MEDICAL_CODING.value, 'Medical Coding'),
        (BlogCategory.HEALTHCARE_TECHNOLOGY.value, 'Healthcare Technology'),
        (BlogCategory.COMPLIANCE.value, 'Compliance'),
        (BlogCategory.REVENUE_CYCLE.value, 'Revenue Cycle'),
        (BlogCategory.INDUSTRY_NEWS.value, 'Industry News'),
        (BlogCategory.TIPS_AND_GUIDES.value, 'Tips and Guides'),
        (BlogCategory.CASE_STUDIES.value, 'Case Studies')
    ], validators=[DataRequired()])
    
    status = SelectField('Status', choices=[
        (BlogStatus.DRAFT.value, 'Draft'),
        (BlogStatus.PUBLISHED.value, 'Published'),
        (BlogStatus.ARCHIVED.value, 'Archived')
    ], validators=[DataRequired()])
    
    featured = BooleanField('Featured Post')
    
    featured_image = StringField('Featured Image URL', validators=[Optional(), URL()],
                                render_kw={'placeholder': 'https://example.com/image.jpg'})
    
    author = StringField('Author', validators=[Optional(), Length(max=100)],
                        render_kw={'placeholder': 'Author name'})
    
    author_image = StringField('Author Image URL', validators=[Optional(), URL()],
                              render_kw={'placeholder': 'https://example.com/author.jpg'})
    
    canonical_url = StringField('Canonical URL', validators=[Optional(), URL()],
                               render_kw={'placeholder': 'https://example.com/original-post (if reposted)'})
    
    linkedin_post = TextAreaField('LinkedIn Post', validators=[Optional(), Length(max=3000)],
                                 render_kw={'rows': 4, 'placeholder': 'Social media post for LinkedIn'})
    
    twitter_post = TextAreaField('Twitter/X Post', validators=[Optional(), Length(max=280)],
                                render_kw={'rows': 3, 'placeholder': 'Social media post for Twitter/X (280 chars max)'})
    
    submit = SubmitField('Save Post')
    publish = SubmitField('Publish Post')
    save_draft = SubmitField('Save as Draft')

class BlogSearchForm(FlaskForm):
    search_query = StringField('Search', validators=[Optional()],
                              render_kw={'placeholder': 'Search blog posts...'})
    
    category_filter = SelectField('Category', choices=[
        ('', 'All Categories'),
        (BlogCategory.MEDICAL_BILLING.value, 'Medical Billing'),
        (BlogCategory.MEDICAL_CODING.value, 'Medical Coding'),
        (BlogCategory.HEALTHCARE_TECHNOLOGY.value, 'Healthcare Technology'),
        (BlogCategory.COMPLIANCE.value, 'Compliance'),
        (BlogCategory.REVENUE_CYCLE.value, 'Revenue Cycle'),
        (BlogCategory.INDUSTRY_NEWS.value, 'Industry News'),
        (BlogCategory.TIPS_AND_GUIDES.value, 'Tips and Guides'),
        (BlogCategory.CASE_STUDIES.value, 'Case Studies')
    ])
    
    status_filter = SelectField('Status', choices=[
        ('', 'All Statuses'),
        (BlogStatus.DRAFT.value, 'Draft'),
        (BlogStatus.PUBLISHED.value, 'Published'),
        (BlogStatus.ARCHIVED.value, 'Archived')
    ])
    
    featured_only = BooleanField('Featured Only')
    
    submit = SubmitField('Search')

class BlogCommentForm(FlaskForm):
    author_name = StringField('Name', validators=[DataRequired(), Length(max=100)],
                             render_kw={'placeholder': 'Your name'})
    
    author_email = StringField('Email', validators=[DataRequired(), Length(max=200)],
                              render_kw={'placeholder': 'your@email.com'})
    
    content = TextAreaField('Comment', validators=[DataRequired(), Length(max=1000)],
                           render_kw={'rows': 4, 'placeholder': 'Share your thoughts...'})
    
    submit = SubmitField('Post Comment')

class BlogCommentModerationForm(FlaskForm):
    action = HiddenField()
    comment_id = HiddenField()
    submit = SubmitField('Moderate')

class BulkActionForm(FlaskForm):
    action = SelectField('Bulk Action', choices=[
        ('', 'Select Action'),
        ('publish', 'Publish'),
        ('unpublish', 'Unpublish (Draft)'),
        ('archive', 'Archive'),
        ('delete', 'Delete')
    ])
    
    selected_posts = HiddenField('Selected Posts')
    submit = SubmitField('Apply')
