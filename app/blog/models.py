from datetime import datetime
from enum import Enum
from flask import current_app
from ..utils.file_ops import read_json, write_json
import uuid
import re
from typing import List, Dict, Optional

class BlogStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class BlogCategory(Enum):
    MEDICAL_BILLING = "Medical Billing"
    MEDICAL_CODING = "Medical Coding"
    HEALTHCARE_TECHNOLOGY = "Healthcare Technology"
    COMPLIANCE = "Compliance"
    REVENUE_CYCLE = "Revenue Cycle"
    INDUSTRY_NEWS = "Industry News"
    TIPS_AND_GUIDES = "Tips and Guides"
    CASE_STUDIES = "Case Studies"

class BlogPost:
    def __init__(self, id=None, title="", slug="", content="", excerpt="", 
                 meta_description="", keywords=None, category=BlogCategory.MEDICAL_BILLING,
                 status=BlogStatus.DRAFT, featured_image="", author="", author_image="",
                 read_time="5 min read", linkedin_post="", twitter_post="",
                 created_at=None, updated_at=None, published_at=None,
                 created_by="", updated_by="", tags=None, seo_title="",
                 canonical_url="", featured=False, view_count=0):
        
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.slug = slug or self._generate_slug(title)
        self.content = content
        self.excerpt = excerpt
        self.meta_description = meta_description
        self.keywords = keywords or []
        self.category = category if isinstance(category, BlogCategory) else BlogCategory(category)
        self.status = status if isinstance(status, BlogStatus) else BlogStatus(status)
        self.featured_image = featured_image
        self.author = author
        self.author_image = author_image
        self.read_time = read_time
        self.linkedin_post = linkedin_post
        self.twitter_post = twitter_post
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()
        self.published_at = published_at
        self.created_by = created_by
        self.updated_by = updated_by
        self.tags = tags or []
        self.seo_title = seo_title or title
        self.canonical_url = canonical_url
        self.featured = featured
        self.view_count = view_count

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        if not title:
            return ""
        
        # Convert to lowercase and replace spaces with hyphens
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')

    def to_dict(self) -> Dict:
        """Convert blog post to dictionary for storage"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'excerpt': self.excerpt,
            'meta_description': self.meta_description,
            'keywords': self.keywords,
            'category': self.category.value,
            'status': self.status.value,
            'featured_image': self.featured_image,
            'author': self.author,
            'author_image': self.author_image,
            'read_time': self.read_time,
            'linkedin_post': self.linkedin_post,
            'twitter_post': self.twitter_post,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'published_at': self.published_at,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'tags': self.tags,
            'seo_title': self.seo_title,
            'canonical_url': self.canonical_url,
            'featured': self.featured,
            'view_count': self.view_count
        }

    @staticmethod
    def from_dict(data: Dict) -> 'BlogPost':
        """Create BlogPost instance from dictionary"""
        return BlogPost(**data)

    def save(self) -> None:
        """Save blog post to storage"""
        self.updated_at = datetime.utcnow().isoformat()
        
        # Set published_at when first published
        if self.status == BlogStatus.PUBLISHED and not self.published_at:
            self.published_at = datetime.utcnow().isoformat()
        
        posts = read_json(current_app.config['BLOG_POSTS_FILE'])
        posts[self.id] = self.to_dict()
        write_json(current_app.config['BLOG_POSTS_FILE'], posts)

    @staticmethod
    def get(post_id: str) -> Optional['BlogPost']:
        """Get blog post by ID"""
        posts = read_json(current_app.config['BLOG_POSTS_FILE'])
        post_data = posts.get(post_id)
        if post_data:
            return BlogPost.from_dict(post_data)
        return None

    @staticmethod
    def get_by_slug(slug: str) -> Optional['BlogPost']:
        """Get blog post by slug"""
        posts = read_json(current_app.config['BLOG_POSTS_FILE'])
        for post_data in posts.values():
            if post_data.get('slug') == slug:
                return BlogPost.from_dict(post_data)
        return None

    @staticmethod
    def get_all(status: Optional[BlogStatus] = None, category: Optional[BlogCategory] = None,
                featured_only: bool = False) -> List['BlogPost']:
        """Get all blog posts with optional filtering"""
        posts = read_json(current_app.config['BLOG_POSTS_FILE'])
        blog_posts = [BlogPost.from_dict(data) for data in posts.values()]
        
        # Apply filters
        if status:
            blog_posts = [post for post in blog_posts if post.status == status]
        
        if category:
            blog_posts = [post for post in blog_posts if post.category == category]
        
        if featured_only:
            blog_posts = [post for post in blog_posts if post.featured]
        
        # Sort by created_at (newest first)
        return sorted(blog_posts, key=lambda x: x.created_at, reverse=True)

    @staticmethod
    def get_published() -> List['BlogPost']:
        """Get all published blog posts"""
        return BlogPost.get_all(status=BlogStatus.PUBLISHED)

    @staticmethod
    def get_featured(limit: int = 3) -> List['BlogPost']:
        """Get featured published blog posts"""
        posts = BlogPost.get_all(status=BlogStatus.PUBLISHED, featured_only=True)
        return posts[:limit]

    @staticmethod
    def get_recent(limit: int = 5) -> List['BlogPost']:
        """Get recent published blog posts"""
        posts = BlogPost.get_published()
        return posts[:limit]

    @staticmethod
    def get_by_category(category: BlogCategory) -> List['BlogPost']:
        """Get published posts by category"""
        return BlogPost.get_all(status=BlogStatus.PUBLISHED, category=category)

    @staticmethod
    def search(query: str) -> List['BlogPost']:
        """Search published blog posts by title, content, or tags"""
        query = query.lower()
        posts = BlogPost.get_published()
        
        results = []
        for post in posts:
            if (query in post.title.lower() or 
                query in post.content.lower() or 
                query in post.excerpt.lower() or
                any(query in tag.lower() for tag in post.tags) or
                any(query in keyword.lower() for keyword in post.keywords)):
                results.append(post)
        
        return results

    @staticmethod
    def get_related(current_post_id: str, limit: int = 3) -> List['BlogPost']:
        """Get related posts based on category and tags"""
        current_post = BlogPost.get(current_post_id)
        if not current_post:
            return []
        
        all_posts = BlogPost.get_published()
        related_posts = []
        
        for post in all_posts:
            if post.id == current_post_id:
                continue
            
            score = 0
            
            # Same category gets higher score
            if post.category == current_post.category:
                score += 3
            
            # Shared tags get points
            shared_tags = set(post.tags) & set(current_post.tags)
            score += len(shared_tags)
            
            # Shared keywords get points
            shared_keywords = set(post.keywords) & set(current_post.keywords)
            score += len(shared_keywords)
            
            if score > 0:
                related_posts.append((post, score))
        
        # Sort by score and return top results
        related_posts.sort(key=lambda x: x[1], reverse=True)
        return [post for post, score in related_posts[:limit]]

    def delete(self) -> bool:
        """Delete blog post"""
        posts = read_json(current_app.config['BLOG_POSTS_FILE'])
        if self.id in posts:
            del posts[self.id]
            write_json(current_app.config['BLOG_POSTS_FILE'], posts)
            return True
        return False

    def publish(self) -> None:
        """Publish the blog post"""
        self.status = BlogStatus.PUBLISHED
        if not self.published_at:
            self.published_at = datetime.utcnow().isoformat()
        self.save()

    def unpublish(self) -> None:
        """Unpublish the blog post (set to draft)"""
        self.status = BlogStatus.DRAFT
        self.save()

    def archive(self) -> None:
        """Archive the blog post"""
        self.status = BlogStatus.ARCHIVED
        self.save()

    def increment_view_count(self) -> None:
        """Increment view count when post is viewed"""
        self.view_count += 1
        # Update only view count without changing updated_at
        posts = read_json(current_app.config['BLOG_POSTS_FILE'])
        if self.id in posts:
            posts[self.id]['view_count'] = self.view_count
            write_json(current_app.config['BLOG_POSTS_FILE'], posts)

    def get_formatted_date(self, field: str = 'created_at') -> str:
        """Get formatted date string"""
        date_str = getattr(self, field)
        if date_str:
            try:
                date_obj = datetime.fromisoformat(date_str)
                return date_obj.strftime('%B %d, %Y')
            except:
                return date_str
        return ""

    def get_url(self) -> str:
        """Get public URL for the blog post"""
        return f"/resources/blog/{self.slug}"

    def get_admin_url(self) -> str:
        """Get admin URL for editing the blog post"""
        return f"/admin/blog/{self.id}/edit"

    def is_published(self) -> bool:
        """Check if post is published"""
        return self.status == BlogStatus.PUBLISHED

    def word_count(self) -> int:
        """Get approximate word count of content"""
        return len(self.content.split())

    def estimated_read_time(self) -> str:
        """Calculate estimated read time based on word count"""
        words = self.word_count()
        minutes = max(1, round(words / 200))  # Average reading speed: 200 words per minute
        return f"{minutes} min read"

class BlogComment:
    """Simple blog comment system"""
    def __init__(self, id=None, post_id="", author_name="", author_email="", 
                 content="", status="pending", created_at=None, ip_address="",
                 user_agent=""):
        self.id = id or str(uuid.uuid4())
        self.post_id = post_id
        self.author_name = author_name
        self.author_email = author_email
        self.content = content
        self.status = status  # pending, approved, rejected, spam
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.ip_address = ip_address
        self.user_agent = user_agent

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'post_id': self.post_id,
            'author_name': self.author_name,
            'author_email': self.author_email,
            'content': self.content,
            'status': self.status,
            'created_at': self.created_at,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }

    @staticmethod
    def from_dict(data: Dict) -> 'BlogComment':
        return BlogComment(**data)

    def save(self) -> None:
        comments = read_json(current_app.config['BLOG_COMMENTS_FILE'])
        comments[self.id] = self.to_dict()
        write_json(current_app.config['BLOG_COMMENTS_FILE'], comments)

    @staticmethod
    def get_by_post(post_id: str, approved_only: bool = True) -> List['BlogComment']:
        """Get comments for a specific post"""
        comments = read_json(current_app.config['BLOG_COMMENTS_FILE'])
        post_comments = []
        
        for comment_data in comments.values():
            if comment_data.get('post_id') == post_id:
                if not approved_only or comment_data.get('status') == 'approved':
                    post_comments.append(BlogComment.from_dict(comment_data))
        
        return sorted(post_comments, key=lambda x: x.created_at)
