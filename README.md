# ardurHealthcare

## Project Overview
ardurHealthcare is a Flask web application designed to provide healthcare-related information and services. It features user authentication, a contact form, various informational pages, and an interactive USA map for exploring state-specific medical billing services, all built with a responsive design using Tailwind CSS.

## Project Structure
```
ardurHealthcare
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── routes.py
│   │   └── templates
│   │       ├── login.html
│   │       └── signup.html
│   ├── main
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates
│   │       ├── about.html
│   │       ├── home.html
│   │       ├── resources.html
│   │       └── services.html
│   ├── contact
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   │       └── templates
│   │           └── contact.html
│   ├── templates
│   │   └── base.html
│   ├── utils
│   │   ├── __init__.py
│   │   └── file_ops.py
│   └── config.py
├── static
│   ├── css
│   │   └── style.css
│   └── js
│       └── script.js
├── run.py
├── requirements.txt
└── README.md
```

## Features
- **User Authentication**: Users can sign up and log in to access certain features.
- **Contact Form**: Users can submit inquiries through a contact form, which are stored locally.
- **Informational Pages**: The application includes pages for Home, About, Services, and Resources.
- **Interactive USA Map**: Click on any state to explore state-specific medical billing services with dynamic content.
- **State-Specific Content**: Dynamic pages with tailored information for each state's healthcare landscape.
- **Responsive Design**: The application is built using Tailwind CSS for a mobile-friendly experience.
- **Accessibility**: Full keyboard navigation and screen reader support for the interactive map.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ardurHealthcare
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python run.py
   ```

## Usage
- Navigate to `http://127.0.0.1:5000` in your web browser to access the application.
- Use the navigation bar to explore different pages.
- Sign up or log in to access authenticated features.
- Submit inquiries through the contact form.

## Interactive Map Feature
The interactive USA map allows users to explore medical billing services across different states:

- **SVG-based Map**: Clean, scalable vector graphics optimized for all devices
- **Click Navigation**: Navigate to state-specific pages by clicking on any state
- **Dynamic Content**: State-specific information loaded from JSON data files
- **Hover Effects**: Visual feedback with tooltips showing state information
- **Accessibility**: Full keyboard navigation and screen reader support
- **Mobile Optimized**: Touch-friendly interactions for mobile devices

### Map Data Structure
State-specific data is stored in `/data/states/state_data.json` and includes:
- State-specific payers and insurance information
- Local healthcare services and specialties
- FAQ sections tailored to each state
- EHR software compatibility information

### Adding New States
To add a new state to the interactive map:
1. Update the state data in `/data/states/state_data.json`
2. Add the state to the URL mapping in the JavaScript code
3. Ensure the state exists in the SVG file with proper ID

For detailed implementation information, see `/docs/INTERACTIVE_MAP_GUIDE.md`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.