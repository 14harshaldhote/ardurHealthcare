#!/usr/bin/env python3
"""
Script to create an admin user for the Ardur Healthcare system
"""

import json
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin_user():
    # Create admin user data
    admin_data = {
        "admin": {
            "email": "admin@ardurhealthcare.com",
            "password_hash": generate_password_hash("admin123"),
            "role": "admin",
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True,
            "profile": {
                "first_name": "Admin",
                "last_name": "User",
                "phone": "555-0123",
                "company": "Ardur Healthcare",
                "notes": "System Administrator"
            }
        }
    }
    
    # Write to users.json
    with open('data/users.json', 'w') as f:
        json.dump(admin_data, f, indent=2)
    
    print("✅ Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
    print("Role: Admin")
    print("\nYou can now log in and access all features including:")
    print("- User Management (/admin/dashboard)")
    print("- CRM System (/crm/dashboard)")
    print("- Blog Management (/admin/blog/)")
    print("- Analytics (/analytics/dashboard)")

if __name__ == "__main__":
    create_admin_user()
