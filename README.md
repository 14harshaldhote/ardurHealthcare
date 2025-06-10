# ardurHealthcare

## Project Overview
ardurHealthcare is a Flask web application designed to provide healthcare-related information and services. It features user authentication, a contact form, and various informational pages, all built with a responsive design using Bootstrap.

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
- **Responsive Design**: The application is built using Bootstrap for a mobile-friendly experience.

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

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.