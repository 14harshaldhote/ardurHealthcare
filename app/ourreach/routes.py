import json
import os
from flask import Blueprint, render_template, abort, current_app
from slugify import slugify

# Create Blueprint
ourreach = Blueprint('ourreach', __name__, template_folder='templates')

def load_state_data():
    """Load all state data from JSON files"""
    state_data = {}

    # Get the path to the data directory
    data_dir = os.path.join(os.path.dirname(current_app.root_path), 'data', 'states')

    # List of JSON files containing state data
    json_files = [
        'state_data.json',
        'additional_states.json',
        'additional_states_2.json',
        'additional_states_3.json',
        'additional_states_4.json',
        'additional_states_5.json',
        'additional_states_6.json'
    ]

    # Load data from each JSON file
    for json_file in json_files:
        file_path = os.path.join(data_dir, json_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state_data.update(data)
            except (json.JSONDecodeError, IOError) as e:
                current_app.logger.error(f"Error loading {json_file}: {e}")

    return state_data

def generate_state_url(state_name):
    """Generate SEO-friendly URL for a state"""
    # Use underscores to match JSON data structure
    state_slug = state_name.lower().replace(' ', '_').replace(',', '').replace('.', '')
    return f"medical-billing-services-in-{state_slug}"

def get_state_by_url(url_slug):
    """Get state data by URL slug"""
    state_data = load_state_data()

    # Extract state name from URL slug
    for state_key, state_info in state_data.items():
        expected_slug = generate_state_url(state_info['name'])
        if url_slug == expected_slug:
            return state_key, state_info

    return None, None

@ourreach.route('/')
def index():
    """Main ourreach page with interactive map"""
    state_data = load_state_data()

    # Prepare state data for the template with URL slugs
    states_with_urls = {}
    for state_key, state_info in state_data.items():
        state_info_copy = state_info.copy()
        state_info_copy['url_slug'] = generate_state_url(state_info['name'])
        states_with_urls[state_key] = state_info_copy

    return render_template('outreach/index.html', states=states_with_urls)

@ourreach.route('/states')
def states_list():
    """List all available states"""
    state_data = load_state_data()

    # Sort states alphabetically and add URL slugs
    sorted_states = []
    for state_key, state_info in state_data.items():
        state_info_copy = state_info.copy()
        state_info_copy['key'] = state_key
        state_info_copy['url_slug'] = generate_state_url(state_info['name'])
        sorted_states.append(state_info_copy)

    sorted_states.sort(key=lambda x: x['name'])

    return render_template('outreach/states_list.html', states=sorted_states)

@ourreach.route('/<state_slug>')
def state_page(state_slug):
    """Individual state page"""
    state_key, state_data = get_state_by_url(state_slug)

    if not state_data:
        abort(404)

    # Add additional data for the template
    state_data['key'] = state_key
    state_data['url_slug'] = state_slug

    return render_template('outreach/state_page.html', state=state_data)

@ourreach.context_processor
def utility_processor():
    """Add utility functions to template context"""
    return dict(
        generate_state_url=generate_state_url,
        load_state_data=load_state_data
    )

# Error handlers
@ourreach.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors for ourreach pages"""
    return render_template('errors/404.html'), 404

@ourreach.errorhandler(500)
def internal_error(error):
    """Handle 500 errors for ourreach pages"""
    return render_template('errors/500.html'), 500
