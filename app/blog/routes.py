from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from . import blog
from .models import BlogPost, BlogComment, BlogStatus, BlogCategory
from .forms import BlogPostForm, BlogSearchForm, BlogCommentForm, BulkActionForm
from ..auth.models import Permission
from ..auth.routes import require_permission
import json
from datetime import datetime

@blog.route('/')
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def dashboard():
    """Blog management dashboard"""
    try:
        # Get all posts
        all_posts = BlogPost.get_all()
        
        # Calculate statistics
        total_posts = len(all_posts)
        published_posts = len([p for p in all_posts if p.status == BlogStatus.PUBLISHED])
        draft_posts = len([p for p in all_posts if p.status == BlogStatus.DRAFT])
        archived_posts = len([p for p in all_posts if p.status == BlogStatus.ARCHIVED])
        
        # Recent posts
        recent_posts = all_posts[:10]
        
        # Popular posts (by view count)
        popular_posts = sorted(all_posts, key=lambda p: p.view_count, reverse=True)[:10]
        
        # Posts by category
        category_stats = {}
        for category in BlogCategory:
            category_posts = [p for p in all_posts if p.category == category]
            category_stats[category.value] = len(category_posts)
        
        dashboard_stats = {
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'archived_posts': archived_posts,
            'recent_posts': recent_posts,
            'popular_posts': popular_posts,
            'category_stats': category_stats
        }
        
        return render_template('blog/dashboard.html', stats=dashboard_stats)
        
    except Exception as e:
        current_app.logger.error(f"Error loading blog dashboard: {str(e)}")
        flash('Error loading blog dashboard', 'error')
        return render_template('blog/dashboard.html', stats={})

@blog.route('/posts')
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def posts():
    """List all blog posts with filtering and search"""
    form = BlogSearchForm()
    bulk_form = BulkActionForm()
    
    # Get all posts
    posts = BlogPost.get_all()
    
    # Apply search filter
    if form.validate_on_submit() and form.search_query.data:
        query = form.search_query.data.lower()
        posts = [p for p in posts if (
            query in p.title.lower() or
            query in p.content.lower() or
            query in p.excerpt.lower() or
            query in ' '.join(p.tags).lower() or
            query in ' '.join(p.keywords).lower()
        )]
    
    # Apply category filter
    if request.args.get('category'):
        category = request.args.get('category')
        posts = [p for p in posts if p.category.value == category]
        form.category_filter.data = category
    
    # Apply status filter
    if request.args.get('status'):
        status = request.args.get('status')
        posts = [p for p in posts if p.status.value == status]
        form.status_filter.data = status
    
    # Apply featured filter
    if request.args.get('featured') == 'true':
        posts = [p for p in posts if p.featured]
        form.featured_only.data = True
    
    # Sort posts (newest first by default)
    sort_by = request.args.get('sort', 'created_at')
    reverse = request.args.get('order', 'desc') == 'desc'
    
    if sort_by == 'title':
        posts.sort(key=lambda p: p.title.lower(), reverse=reverse)
    elif sort_by == 'status':
        posts.sort(key=lambda p: p.status.value, reverse=reverse)
    elif sort_by == 'category':
        posts.sort(key=lambda p: p.category.value, reverse=reverse)
    elif sort_by == 'view_count':
        posts.sort(key=lambda p: p.view_count, reverse=reverse)
    else:  # created_at
        posts.sort(key=lambda p: p.created_at, reverse=reverse)
    
    return render_template('blog/posts.html', posts=posts, form=form, bulk_form=bulk_form)

@blog.route('/posts/create', methods=['GET', 'POST'])
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def create_post():
    """Create a new blog post"""
    form = BlogPostForm()
    
    if form.validate_on_submit():
        # Process keywords and tags
        keywords = [k.strip() for k in form.keywords.data.split(',') if k.strip()] if form.keywords.data else []
        tags = [t.strip() for t in form.tags.data.split(',') if t.strip()] if form.tags.data else []
        
        # Determine status based on button clicked
        status = BlogStatus.DRAFT
        if 'publish' in request.form:
            status = BlogStatus.PUBLISHED
        elif form.status.data:
            status = BlogStatus(form.status.data)
        
        # Create blog post
        post = BlogPost(
            title=form.title.data,
            slug=form.slug.data,
            content=form.content.data,
            excerpt=form.excerpt.data,
            meta_description=form.meta_description.data,
            seo_title=form.seo_title.data,
            keywords=keywords,
            tags=tags,
            category=BlogCategory(form.category.data),
            status=status,
            featured=form.featured.data,
            featured_image=form.featured_image.data,
            author=form.author.data or current_user.username,
            author_image=form.author_image.data,
            canonical_url=form.canonical_url.data,
            linkedin_post=form.linkedin_post.data,
            twitter_post=form.twitter_post.data,
            created_by=current_user.username,
            updated_by=current_user.username
        )
        
        # Auto-generate read time
        post.read_time = post.estimated_read_time()
        
        post.save()
        
        action = "published" if status == BlogStatus.PUBLISHED else "saved as draft"
        flash(f'Blog post "{post.title}" {action} successfully!', 'success')
        return redirect(url_for('blog.view_post', post_id=post.id))
    
    # Set default values
    form.author.data = current_user.username
    form.status.data = BlogStatus.DRAFT.value
    
    return render_template('blog/create_post.html', form=form)

@blog.route('/posts/<post_id>')
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def view_post(post_id):
    """View blog post details"""
    post = BlogPost.get(post_id)
    if not post:
        flash('Blog post not found.', 'error')
        return redirect(url_for('blog.posts'))
    
    # Get comments for this post
    comments = BlogComment.get_by_post(post_id, approved_only=False)
    
    return render_template('blog/view_post.html', post=post, comments=comments)

@blog.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def edit_post(post_id):
    """Edit blog post"""
    post = BlogPost.get(post_id)
    if not post:
        flash('Blog post not found.', 'error')
        return redirect(url_for('blog.posts'))
    
    form = BlogPostForm(obj=post)
    
    if form.validate_on_submit():
        # Process keywords and tags
        keywords = [k.strip() for k in form.keywords.data.split(',') if k.strip()] if form.keywords.data else []
        tags = [t.strip() for t in form.tags.data.split(',') if t.strip()] if form.tags.data else []
        
        # Determine status based on button clicked
        if 'publish' in request.form:
            post.status = BlogStatus.PUBLISHED
        elif 'save_draft' in request.form:
            post.status = BlogStatus.DRAFT
        elif form.status.data:
            post.status = BlogStatus(form.status.data)
        
        # Update post data
        post.title = form.title.data
        post.slug = form.slug.data or post._generate_slug(form.title.data)
        post.content = form.content.data
        post.excerpt = form.excerpt.data
        post.meta_description = form.meta_description.data
        post.seo_title = form.seo_title.data
        post.keywords = keywords
        post.tags = tags
        post.category = BlogCategory(form.category.data)
        post.featured = form.featured.data
        post.featured_image = form.featured_image.data
        post.author = form.author.data
        post.author_image = form.author_image.data
        post.canonical_url = form.canonical_url.data
        post.linkedin_post = form.linkedin_post.data
        post.twitter_post = form.twitter_post.data
        post.updated_by = current_user.username
        
        # Update read time
        post.read_time = post.estimated_read_time()
        
        post.save()
        
        flash(f'Blog post "{post.title}" updated successfully!', 'success')
        return redirect(url_for('blog.view_post', post_id=post.id))
    
    # Pre-populate form
    form.keywords.data = ', '.join(post.keywords)
    form.tags.data = ', '.join(post.tags)
    form.category.data = post.category.value
    form.status.data = post.status.value
    
    return render_template('blog/edit_post.html', form=form, post=post)

@blog.route('/posts/<post_id>/delete', methods=['POST'])
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def delete_post(post_id):
    """Delete blog post"""
    post = BlogPost.get(post_id)
    if not post:
        return jsonify({'error': 'Blog post not found'}), 404
    
    title = post.title
    if post.delete():
        return jsonify({'message': f'Blog post "{title}" deleted successfully'})
    else:
        return jsonify({'error': 'Failed to delete blog post'}), 500

@blog.route('/posts/<post_id>/publish', methods=['POST'])
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def publish_post(post_id):
    """Publish a blog post"""
    post = BlogPost.get(post_id)
    if not post:
        return jsonify({'error': 'Blog post not found'}), 404
    
    post.publish()
    return jsonify({'message': f'Blog post "{post.title}" published successfully'})

@blog.route('/posts/<post_id>/unpublish', methods=['POST'])
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def unpublish_post(post_id):
    """Unpublish a blog post"""
    post = BlogPost.get(post_id)
    if not post:
        return jsonify({'error': 'Blog post not found'}), 404
    
    post.unpublish()
    return jsonify({'message': f'Blog post "{post.title}" unpublished successfully'})

@blog.route('/posts/<post_id>/archive', methods=['POST'])
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def archive_post(post_id):
    """Archive a blog post"""
    post = BlogPost.get(post_id)
    if not post:
        return jsonify({'error': 'Blog post not found'}), 404
    
    post.archive()
    return jsonify({'message': f'Blog post "{post.title}" archived successfully'})

@blog.route('/posts/bulk-action', methods=['POST'])
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def bulk_action():
    """Perform bulk actions on blog posts"""
    form = BulkActionForm()
    
    if form.validate_on_submit():
        action = form.action.data
        selected_posts = form.selected_posts.data.split(',') if form.selected_posts.data else []
        
        if not action or not selected_posts:
            flash('Please select an action and at least one post.', 'error')
            return redirect(url_for('blog.posts'))
        
        success_count = 0
        for post_id in selected_posts:
            post = BlogPost.get(post_id.strip())
            if post:
                try:
                    if action == 'publish':
                        post.publish()
                    elif action == 'unpublish':
                        post.unpublish()
                    elif action == 'archive':
                        post.archive()
                    elif action == 'delete':
                        post.delete()
                    
                    success_count += 1
                except Exception as e:
                    current_app.logger.error(f"Error performing bulk action {action} on post {post_id}: {str(e)}")
        
        flash(f'Bulk action completed successfully on {success_count} posts.', 'success')
    
    return redirect(url_for('blog.posts'))

@blog.route('/comments')
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def comments():
    """Manage blog comments"""
    # This would be implemented if comments system is needed
    return render_template('blog/comments.html', comments=[])

@blog.route('/analytics')
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def analytics():
    """Blog analytics and insights"""
    try:
        posts = BlogPost.get_all()
        
        # Calculate analytics
        total_views = sum(post.view_count for post in posts)
        avg_views = total_views / len(posts) if posts else 0
        
        # Most popular posts
        popular_posts = sorted(posts, key=lambda p: p.view_count, reverse=True)[:10]
        
        # Posts by status
        status_stats = {}
        for status in BlogStatus:
            status_posts = [p for p in posts if p.status == status]
            status_stats[status.value] = len(status_posts)
        
        # Posts by category
        category_stats = {}
        for category in BlogCategory:
            category_posts = [p for p in posts if p.category == category]
            category_stats[category.value] = {
                'count': len(category_posts),
                'views': sum(p.view_count for p in category_posts)
            }
        
        # Monthly publishing stats (last 12 months)
        monthly_stats = {}
        for post in posts:
            if post.published_at:
                try:
                    date = datetime.fromisoformat(post.published_at)
                    month_key = date.strftime('%Y-%m')
                    monthly_stats[month_key] = monthly_stats.get(month_key, 0) + 1
                except:
                    pass
        
        analytics_data = {
            'total_posts': len(posts),
            'total_views': total_views,
            'avg_views': round(avg_views, 1),
            'popular_posts': popular_posts,
            'status_stats': status_stats,
            'category_stats': category_stats,
            'monthly_stats': monthly_stats
        }
        
        return render_template('blog/analytics.html', data=analytics_data)
        
    except Exception as e:
        current_app.logger.error(f"Error loading blog analytics: {str(e)}")
        flash('Error loading blog analytics', 'error')
        return render_template('blog/analytics.html', data={})

@blog.route('/export')
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def export_posts():
    """Export blog posts to CSV"""
    try:
        from flask import Response
        import csv
        import io
        
        posts = BlogPost.get_all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Title', 'Slug', 'Category', 'Status', 'Author',
            'Created At', 'Published At', 'View Count', 'Featured',
            'Keywords', 'Tags', 'Excerpt'
        ])
        
        # Write data
        for post in posts:
            writer.writerow([
                post.id, post.title, post.slug, post.category.value, post.status.value,
                post.author, post.get_formatted_date('created_at'),
                post.get_formatted_date('published_at') if post.published_at else '',
                post.view_count, post.featured, ', '.join(post.keywords),
                ', '.join(post.tags), post.excerpt
            ])
        
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=blog_posts_export.csv'}
        )
        
    except Exception as e:
        current_app.logger.error(f"Error exporting blog posts: {str(e)}")
        flash('Error exporting blog posts', 'error')
        return redirect(url_for('blog.posts'))

# API Routes for frontend integration
@blog.route('/api/posts')
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def api_posts():
    """API endpoint for blog posts (for AJAX requests)"""
    try:
        posts = BlogPost.get_all()
        posts_data = []
        
        for post in posts:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'slug': post.slug,
                'status': post.status.value,
                'category': post.category.value,
                'author': post.author,
                'created_at': post.get_formatted_date(),
                'view_count': post.view_count,
                'featured': post.featured,
                'url': post.get_url(),
                'admin_url': post.get_admin_url()
            })
        
        return jsonify({
            'success': True,
            'posts': posts_data,
            'count': len(posts_data)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching posts API: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Unable to fetch posts'
        }), 500

@blog.route('/api/posts/<post_id>/preview')
@login_required
@require_permission(Permission.SYSTEM_ADMIN)
def api_preview_post(post_id):
    """API endpoint for blog post preview"""
    post = BlogPost.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    return jsonify({
        'success': True,
        'post': {
            'title': post.title,
            'content': post.content,
            'excerpt': post.excerpt,
            'author': post.author,
            'category': post.category.value,
            'tags': post.tags,
            'created_at': post.get_formatted_date(),
            'read_time': post.read_time
        }
    })
