from flask_login import UserMixin
from ..utils.file_ops import read_json, write_json
from flask import current_app
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"
    CLIENT = "client"
    VIEWER = "viewer"

class Permission(Enum):
    # System permissions
    SYSTEM_ADMIN = "system_admin"
    
    # User management
    USER_CREATE = "user_create"
    USER_EDIT = "user_edit"
    USER_DELETE = "user_delete"
    USER_VIEW = "user_view"
    
    # CRM permissions
    CRM_CREATE = "crm_create"
    CRM_EDIT = "crm_edit"
    CRM_DELETE = "crm_delete"
    CRM_VIEW = "crm_view"
    CRM_EXPORT = "crm_export"
    
    # Analytics permissions
    ANALYTICS_VIEW = "analytics_view"
    ANALYTICS_EXPORT = "analytics_export"
    
    # Service management
    SERVICE_MANAGE = "service_manage"
    SERVICE_VIEW = "service_view"

# Role-permission mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.SYSTEM_ADMIN,
        Permission.USER_CREATE, Permission.USER_EDIT, Permission.USER_DELETE, Permission.USER_VIEW,
        Permission.CRM_CREATE, Permission.CRM_EDIT, Permission.CRM_DELETE, Permission.CRM_VIEW, Permission.CRM_EXPORT,
        Permission.ANALYTICS_VIEW, Permission.ANALYTICS_EXPORT,
        Permission.SERVICE_MANAGE, Permission.SERVICE_VIEW
    ],
    UserRole.MANAGER: [
        Permission.USER_VIEW,
        Permission.CRM_CREATE, Permission.CRM_EDIT, Permission.CRM_VIEW, Permission.CRM_EXPORT,
        Permission.ANALYTICS_VIEW, Permission.ANALYTICS_EXPORT,
        Permission.SERVICE_VIEW
    ],
    UserRole.STAFF: [
        Permission.CRM_CREATE, Permission.CRM_EDIT, Permission.CRM_VIEW,
        Permission.ANALYTICS_VIEW,
        Permission.SERVICE_VIEW
    ],
    UserRole.CLIENT: [
        Permission.CRM_VIEW,  # Only their own records
        Permission.SERVICE_VIEW
    ],
    UserRole.VIEWER: [
        Permission.CRM_VIEW,
        Permission.ANALYTICS_VIEW,
        Permission.SERVICE_VIEW
    ]
}

class User(UserMixin):
    def __init__(self, username, email, role=UserRole.CLIENT, created_at=None, is_active=True, profile=None):
        self.id = username
        self.username = username
        self.email = email
        self.role = role if isinstance(role, UserRole) else UserRole(role)
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.is_active = is_active
        self.profile = profile or {}

    def has_permission(self, permission):
        """Check if user has specific permission"""
        if isinstance(permission, str):
            permission = Permission(permission)
        return permission in ROLE_PERMISSIONS.get(self.role, [])

    def has_role(self, role):
        """Check if user has specific role"""
        if isinstance(role, str):
            role = UserRole(role)
        return self.role == role

    def is_admin(self):
        """Check if user is admin"""
        return self.role == UserRole.ADMIN

    def is_manager(self):
        """Check if user is manager or admin"""
        return self.role in [UserRole.ADMIN, UserRole.MANAGER]

    def can_access_crm(self):
        """Check if user can access CRM functionality"""
        return self.has_permission(Permission.CRM_VIEW)

    def can_access_analytics(self):
        """Check if user can access analytics"""
        return self.has_permission(Permission.ANALYTICS_VIEW)

    def to_dict(self):
        """Convert user to dictionary for storage"""
        return {
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at,
            'is_active': self.is_active,
            'profile': self.profile
        }

    @staticmethod
    def get(username):
        users = read_json(current_app.config['USERS_FILE'])
        user_data = users.get(username)
        if user_data:
            return User(
                username=username, 
                email=user_data['email'],
                role=user_data.get('role', 'client'),
                created_at=user_data.get('created_at'),
                is_active=user_data.get('is_active', True),
                profile=user_data.get('profile', {})
            )
        return None

    @staticmethod
    def get_all():
        """Get all users"""
        users = read_json(current_app.config['USERS_FILE'])
        return [
            User(
                username=username,
                email=data['email'],
                role=data.get('role', 'client'),
                created_at=data.get('created_at'),
                is_active=data.get('is_active', True),
                profile=data.get('profile', {})
            )
            for username, data in users.items()
        ]

    def save(self, password_hash=None):
        """Save user to storage"""
        users = read_json(current_app.config['USERS_FILE'])
        user_data = self.to_dict()
        if password_hash:
            user_data['password_hash'] = password_hash
        users[self.username] = user_data
        write_json(current_app.config['USERS_FILE'], users)

    @staticmethod
    def create(username, email, password_hash, role=UserRole.CLIENT, profile=None):
        """Create a new user"""
        user = User(
            username=username,
            email=email,
            role=role,
            profile=profile or {}
        )
        user.save(password_hash)
        return user

    def delete(self):
        """Delete user from storage"""
        users = read_json(current_app.config['USERS_FILE'])
        if self.username in users:
            del users[self.username]
            write_json(current_app.config['USERS_FILE'], users)
            return True
        return False
