import json
import os
from datetime import datetime
from flask import current_app, has_app_context
import logging
import re

def load_blog_data():
    """Load blog data from JSON file"""
    try:
        # Get the path to the JSON file
        if has_app_context():
            json_path = os.path.join(current_app.root_path, '..', 'data', 'blog', 'blog_data.json')
        else:
            # Fallback path when no app context
            json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'blog', 'blog_data.json')

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('blogs', [])
    except Exception as e:
        if has_app_context():
            current_app.logger.error(f"Error loading blog data: {str(e)}")
        else:
            print(f"Error loading blog data: {str(e)}")
        return []

def process_blog_post(blog_data):
    """Process raw blog data into template-friendly format"""
    try:
        # Extract content for excerpt generation
        content_text = ""
        if blog_data.get('content'):
            for section in blog_data['content']:
                if section.get('body'):
                    content_text += section['body'] + " "
                if section.get('h3_sections'):
                    for h3_section in section['h3_sections']:
                        if h3_section.get('body'):
                            content_text += h3_section['body'] + " "

        # Generate excerpt (first 150 characters)
        excerpt = content_text[:150].strip()
        if len(content_text) > 150:
            excerpt += "..."

        # Estimate read time (average 200 words per minute)
        word_count = len(content_text.split())
        read_time = max(1, round(word_count / 200))
        read_time_text = f"{read_time} min read"

        # Extract keywords from meta
        keywords = []
        if blog_data.get('meta', {}).get('keyword'):
            keywords = [kw.strip() for kw in blog_data['meta']['keyword'].split(',')]

        # Set category based on keywords or content
        category = "Medical Billing"
        if any(keyword in ["coding", "cpt", "icd"] for keyword in [k.lower() for k in keywords]):
            category = "Medical Coding"
        elif any(keyword in ["denial", "claims"] for keyword in [k.lower() for k in keywords]):
            category = "Claims Management"
        elif any(keyword in ["process", "workflow"] for keyword in [k.lower() for k in keywords]):
            category = "Billing Process"

        # Format the blog post data
        processed_post = {
            'slug': blog_data.get('slug', ''),
            'title': blog_data.get('title', ''),
            'h1': blog_data.get('h1', blog_data.get('title', '')),
            'meta_description': blog_data.get('meta', {}).get('meta_description', ''),
            'keywords': keywords,
            'excerpt': excerpt,
            'content': blog_data.get('content', []),
            'category': category,
            'author': "Ardur Healthcare Team",
            'date': datetime(2024, 1, 15),  # Default date, can be customized
            'read_time': read_time_text,
            'social': blog_data.get('social', {}),
            'primary_keyword': blog_data.get('meta', {}).get('keyword', ''),
            'linkedin_caption': blog_data.get('social', {}).get('linkedin', ''),
            'twitter_caption': blog_data.get('social', {}).get('twitter', '')
        }

        return processed_post
    except Exception as e:
        if has_app_context():
            current_app.logger.error(f"Error processing blog post: {str(e)}")
        else:
            print(f"Error processing blog post: {str(e)}")
        return None

def get_all_blog_posts():
    """Get all blog posts"""
    try:
        raw_blogs = load_blog_data()
        processed_posts = []

        for blog_data in raw_blogs:
            processed_post = process_blog_post(blog_data)
            if processed_post:
                processed_posts.append(processed_post)

        # Sort by date (newest first) - can be customized based on your needs
        processed_posts.sort(key=lambda x: x['date'], reverse=True)

        return processed_posts
    except Exception as e:
        if has_app_context():
            current_app.logger.error(f"Error getting all blog posts: {str(e)}")
        else:
            print(f"Error getting all blog posts: {str(e)}")
        return []

def get_blog_post(slug):
    """Get a specific blog post by slug"""
    try:
        raw_blogs = load_blog_data()

        for blog_data in raw_blogs:
            if blog_data.get('slug') == slug:
                return process_blog_post(blog_data)

        return None
    except Exception as e:
        if has_app_context():
            current_app.logger.error(f"Error getting blog post '{slug}': {str(e)}")
        else:
            print(f"Error getting blog post '{slug}': {str(e)}")
        return None

def get_related_posts(current_slug, limit=3):
    """Get related posts based on keywords and category"""
    try:
        all_posts = get_all_blog_posts()
        current_post = None

        # Find the current post
        for post in all_posts:
            if post['slug'] == current_slug:
                current_post = post
                break

        if not current_post:
            return all_posts[:limit]

        # Score posts based on similarity
        related_posts = []
        current_keywords = set(kw.lower() for kw in current_post['keywords'])

        for post in all_posts:
            if post['slug'] == current_slug:
                continue

            score = 0
            post_keywords = set(kw.lower() for kw in post['keywords'])

            # Score based on keyword overlap
            common_keywords = current_keywords.intersection(post_keywords)
            score += len(common_keywords) * 3

            # Score based on category match
            if post['category'] == current_post['category']:
                score += 2

            # Score based on title similarity (simple word matching)
            current_title_words = set(current_post['title'].lower().split())
            post_title_words = set(post['title'].lower().split())
            common_title_words = current_title_words.intersection(post_title_words)
            score += len(common_title_words)

            related_posts.append((post, score))

        # Sort by score and return top posts
        related_posts.sort(key=lambda x: x[1], reverse=True)
        return [post for post, score in related_posts[:limit]]

    except Exception as e:
        if has_app_context():
            current_app.logger.error(f"Error getting related posts for '{current_slug}': {str(e)}")
        else:
            print(f"Error getting related posts for '{current_slug}': {str(e)}")
        # Return first few posts as fallback
        all_posts = get_all_blog_posts()
        return [post for post in all_posts if post['slug'] != current_slug][:limit]

def generate_toc(content):
    """Generate table of contents from blog content"""
    try:
        toc = []

        for section in content:
            if section.get('h2'):
                toc_item = {
                    'title': section['h2'],
                    'anchor': section['h2'].lower().replace(' ', '-').replace(':', '').replace('?', '').replace('!', ''),
                    'subsections': []
                }

                if section.get('h3_sections'):
                    for h3_section in section['h3_sections']:
                        if h3_section.get('h3'):
                            toc_item['subsections'].append({
                                'title': h3_section['h3'],
                                'anchor': h3_section['h3'].lower().replace(' ', '-').replace(':', '').replace('?', '').replace('!', '')
                            })

                toc.append(toc_item)

        return toc
    except Exception as e:
        if has_app_context():
            current_app.logger.error(f"Error generating TOC: {str(e)}")
        else:
            print(f"Error generating TOC: {str(e)}")
        return []

def search_posts(query, limit=10):
    """Search posts by title, content, or keywords"""
    try:
        all_posts = get_all_blog_posts()
        query_lower = query.lower()
        results = []

        for post in all_posts:
            score = 0

            # Search in title
            if query_lower in post['title'].lower():
                score += 5

            # Search in keywords
            for keyword in post['keywords']:
                if query_lower in keyword.lower():
                    score += 3

            # Search in excerpt
            if query_lower in post['excerpt'].lower():
                score += 2

            # Search in content
            content_text = ""
            for section in post['content']:
                if section.get('body'):
                    content_text += section['body'] + " "
                if section.get('h3_sections'):
                    for h3_section in section['h3_sections']:
                        if h3_section.get('body'):
                            content_text += h3_section['body'] + " "

            if query_lower in content_text.lower():
                score += 1

            if score > 0:
                results.append((post, score))

        # Sort by score and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return [post for post, score in results[:limit]]

    except Exception as e:
        if has_app_context():
            current_app.logger.error(f"Error searching posts: {str(e)}")
        else:
            print(f"Error searching posts: {str(e)}")
        return []
