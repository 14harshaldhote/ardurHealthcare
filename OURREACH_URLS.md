# OurReach URL Structure Documentation

## Overview
The OurReach module provides state-specific medical billing service pages with an interactive map interface. This module is built using Flask blueprints and serves content from JSON data files.

## URL Structure

### Blueprint Configuration
- **Blueprint Name**: `ourreach`
- **URL Prefix**: `/state`
- **Template Folder**: `app/ourreach/templates/outreach/`

### Available Routes

#### 1. Main Interactive Map Page
- **URL**: `/state/`
- **Route**: `@ourreach.route('/')`
- **Function**: `index()`
- **Template**: `outreach/index.html`
- **Description**: Displays the main page with an interactive US map showing all states

#### 2. States List Page  
- **URL**: `/state/states`
- **Route**: `@ourreach.route('/states')`
- **Function**: `states_list()`
- **Template**: `outreach/states_list.html`
- **Description**: Shows a grid view of all available states with search functionality

#### 3. Individual State Pages
- **URL Pattern**: `/state/medical-billing-services-in-{state-name}`
- **Route**: `@ourreach.route('/<state_slug>')`
- **Function**: `state_page(state_slug)`
- **Template**: `outreach/state_page.html`
- **Description**: Displays detailed information for a specific state

### Example State URLs
```
/state/medical-billing-services-in-alabama
/state/medical-billing-services-in-arkansas
/state/medical-billing-services-in-california
/state/medical-billing-services-in-florida
/state/medical-billing-services-in-texas
```

## Data Structure

### JSON Data Location
- **Path**: `ardurHealthcare/data/states/state_data.json`
- **Additional Files**: `additional_states.json`, `additional_states_2.json`, etc. (if they exist)

### State Data Format
Each state entry contains:
```json
{
  "state_key": {
    "name": "State Name",
    "title": "Medical Billing Services in State Name",
    "subtitle": "Medical Billing & Coding Services for State Name Healthcare Practices",
    "description": "Detailed description...",
    "why_choose_us": ["Reason 1", "Reason 2", ...],
    "payers": ["Payer 1", "Payer 2", ...],
    "services": ["Service 1", "Service 2", ...],
    "specialties": ["Specialty 1", "Specialty 2", ...],
    "software_compatibility": ["Software 1", "Software 2", ...],
    "faqs": [
      {
        "question": "Question text",
        "answer": "Answer text"
      }
    ]
  }
}
```

## URL Generation

### SEO-Friendly URLs
URLs are generated using the `generate_state_url()` function:
- Takes state name (e.g., "Arkansas")
- Converts to lowercase and slugifies
- Prefixes with "medical-billing-services-in-"
- Result: "medical-billing-services-in-arkansas"

### URL Matching
The `get_state_by_url()` function:
- Takes a URL slug
- Matches against all states in the JSON data
- Returns the matching state key and data
- Returns None if no match found (triggers 404)

## Navigation Links

### Template URL References
All templates use Flask's `url_for()` function:
- `{{ url_for('ourreach.index') }}` → `/state/`
- `{{ url_for('ourreach.states_list') }}` → `/state/states`
- `{{ url_for('ourreach.state_page', state_slug=state.url_slug) }}` → `/state/medical-billing-services-in-{state}`

### Navigation Menu
The main navigation includes:
- **"Our Reach"** link → `/state/` (interactive map)

## Error Handling

### 404 Errors
- Invalid state slugs return 404
- Missing JSON files are handled gracefully
- Custom error handlers defined in routes.py

### Template Errors
- Templates expect specific data structure
- Missing data fields may cause rendering issues
- Error handlers redirect to appropriate error pages

## Development Notes

### Important Files
- `app/ourreach/routes.py` - Route definitions and logic
- `app/ourreach/__init__.py` - Blueprint export
- `app/__init__.py` - Blueprint registration
- `app/ourreach/templates/outreach/` - Template files

### Template Structure
```
app/ourreach/templates/outreach/
├── index.html          # Interactive map page
├── states_list.html    # States grid view
├── state_page.html     # Individual state page
└── us_map.svg         # SVG map file
```

### Key Functions
- `load_state_data()` - Loads all state data from JSON files
- `generate_state_url()` - Creates SEO-friendly URLs
- `get_state_by_url()` - Matches URLs to state data
- `utility_processor()` - Adds utility functions to templates

## Testing URLs

### Local Development
When running locally on `http://127.0.0.1:5000`:
- Map page: `http://127.0.0.1:5000/state/`
- States list: `http://127.0.0.1:5000/state/states`
- Arkansas page: `http://127.0.0.1:5000/state/medical-billing-services-in-arkansas`

### Production URLs
For production domain `https://ardurhealthcare.com`:
- Map page: `https://ardurhealthcare.com/state/`
- States list: `https://ardurhealthcare.com/state/states`
- Arkansas page: `https://ardurhealthcare.com/state/medical-billing-services-in-arkansas`
