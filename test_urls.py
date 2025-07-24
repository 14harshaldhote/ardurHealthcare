#!/usr/bin/env python3
"""
Test script to verify URL routing for the resources section
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import url_for

def test_resources_urls():
    """Test all resources-related URLs"""
    app = create_app()

    with app.app_context():
        print("🧪 Testing Resources URL Generation...")

        try:
            # Test main resources URLs
            resources_url = url_for('resources.resources_index')
            print(f"✅ Resources Index: {resources_url}")

            blog_url = url_for('resources.blog')
            print(f"✅ Blog: {blog_url}")

            case_studies_url = url_for('resources.case_studies')
            print(f"✅ Case Studies: {case_studies_url}")

            faqs_url = url_for('resources.faqs')
            print(f"✅ FAQs: {faqs_url}")

            # Test specific blog post URLs
            blog_post_url = url_for('resources.what_is_medical_billing')
            print(f"✅ Blog Post (What is Medical Billing): {blog_post_url}")

            coding_billing_url = url_for('resources.medical_coding_vs_billing')
            print(f"✅ Blog Post (Coding vs Billing): {coding_billing_url}")

            denial_reasons_url = url_for('resources.medical_billing_denial_reasons')
            print(f"✅ Blog Post (Denial Reasons): {denial_reasons_url}")

            cpt_codes_url = url_for('resources.cpt_icd10_hcpcs_codes')
            print(f"✅ Blog Post (CPT/ICD-10/HCPCS): {cpt_codes_url}")

            billing_process_url = url_for('resources.medical_billing_process_overview')
            print(f"✅ Blog Post (Billing Process): {billing_process_url}")

            print("\n🎉 All URLs generated successfully!")
            return True

        except Exception as e:
            print(f"❌ Error generating URLs: {e}")
            return False

def test_route_accessibility():
    """Test that routes are accessible via test client"""
    app = create_app()

    with app.test_client() as client:
        print("\n🧪 Testing Route Accessibility...")

        routes_to_test = [
            ('/resources/', 'Resources Index'),
            ('/resources/blog', 'Blog'),
            ('/resources/case-studies', 'Case Studies'),
            ('/resources/faqs', 'FAQs'),
            ('/resources/blog/what-is-medical-billing', 'What is Medical Billing Blog Post'),
        ]

        all_passed = True

        for route, description in routes_to_test:
            try:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"✅ {description} ({route}): {response.status_code}")
                elif response.status_code == 302:
                    print(f"🔄 {description} ({route}): {response.status_code} (Redirect)")
                else:
                    print(f"⚠️  {description} ({route}): {response.status_code}")
                    all_passed = False
            except Exception as e:
                print(f"❌ {description} ({route}): Error - {e}")
                all_passed = False

        return all_passed

def test_navigation_links():
    """Test that navigation links work in templates"""
    app = create_app()

    with app.test_client() as client:
        print("\n🧪 Testing Navigation Links...")

        try:
            # Test the main page to see if Resources link works
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads successfully")

                # Check if the response contains the resources link
                if b'/resources/' in response.data:
                    print("✅ Resources link found in navigation")
                else:
                    print("⚠️  Resources link not found in navigation")

            # Test the resources page itself
            response = client.get('/resources/')
            if response.status_code == 200:
                print("✅ Resources page loads successfully")

                # Check for key elements
                if b'Resource Center' in response.data:
                    print("✅ Resources page contains expected content")
                if b'Blog' in response.data:
                    print("✅ Blog section found")
                if b'Case Studies' in response.data:
                    print("✅ Case Studies section found")
                if b'FAQs' in response.data:
                    print("✅ FAQs section found")
            else:
                print(f"❌ Resources page failed to load: {response.status_code}")
                return False

            return True

        except Exception as e:
            print(f"❌ Error testing navigation: {e}")
            return False

def main():
    """Run all tests"""
    print("🚀 Starting Resources URL Tests...\n")

    # Test URL generation
    url_test_passed = test_resources_urls()

    # Test route accessibility
    route_test_passed = test_route_accessibility()

    # Test navigation
    nav_test_passed = test_navigation_links()

    print(f"\n📊 Test Results:")
    print(f"URL Generation: {'✅ PASSED' if url_test_passed else '❌ FAILED'}")
    print(f"Route Accessibility: {'✅ PASSED' if route_test_passed else '❌ FAILED'}")
    print(f"Navigation Links: {'✅ PASSED' if nav_test_passed else '❌ FAILED'}")

    if url_test_passed and route_test_passed and nav_test_passed:
        print("\n🎉 All tests passed! Resources section is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    exit(main())
