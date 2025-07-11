# Ardur Healthcare - Enhanced System Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the enhanced Ardur Healthcare system with redesigned state pages, advanced contact forms, and analytics capabilities.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- pip package manager
- Git (for version control)
- Access to SMTP server (Gmail recommended for development)

### Development Environment
- Text editor or IDE (VS Code recommended)
- Web browser for testing
- Terminal/Command prompt access

## Installation Steps

### 1. Clone and Setup Project
```bash
# Clone the repository
git clone <repository-url>
cd ardurHealthcare

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### 3. Create Required Directories
```bash
# Create logs directory for analytics
mkdir -p logs

# Verify data directory exists
ls -la data/
```

### 4. Environment Configuration

#### Create `.env` file (recommended)
```bash
# Create environment file
touch .env
```

#### Add Environment Variables
Add the following to your `.env` file or export them:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Email Recipients
ADMIN_EMAIL=admin@ardurhealthcare.com
ANALYTICS_EMAIL=analytics@ardurhealthcare.com

# Optional: Custom sender
MAIL_DEFAULT_SENDER=noreply@ardurhealthcare.com
```

#### Gmail App Password Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `MAIL_PASSWORD`

### 5. Test the Installation
```bash
# Run the test script
python test_system.py

# Start the development server
python run.py
```

## Configuration Details

### Email System Configuration

#### Development (Gmail)
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
```

#### Production (Custom SMTP)
```python
MAIL_SERVER = 'your-smtp-server.com'
MAIL_PORT = 587  # or 465 for SSL
MAIL_USE_TLS = True  # or False if using SSL
MAIL_USE_SSL = False  # Set to True if using SSL
```

### Analytics Configuration
Analytics data is stored in `logs/analytics_log.json`. No additional configuration required.

## Testing the Deployment

### 1. Access State Pages
Visit: `http://localhost:5000/state/medical-billing-services-in-alabama`

**Expected Results:**
- ✅ Page loads successfully
- ✅ Consolidated services section visible
- ✅ Separate testimonials section
- ✅ Enhanced contact form with multi-select specialties

### 2. Test Contact Form
1. Fill out the contact form completely
2. Select multiple specialties
3. Choose a service type
4. Submit the form

**Expected Results:**
- ✅ Form submits successfully
- ✅ Success message appears
- ✅ Admin receives complete form data email
- ✅ Analytics receives anonymized data email
- ✅ Data logged in `logs/analytics_log.json`

### 3. Test Analytics Dashboard
1. Navigate to: `http://localhost:5000/analytics/dashboard`
2. Login with admin credentials
3. View submission data

**Expected Results:**
- ✅ Dashboard loads with charts
- ✅ Submission data visible
- ✅ Export functionality works

## Troubleshooting

### Common Issues and Solutions

#### 1. Email Not Sending
**Problem:** Contact form submissions not sending emails

**Solutions:**
- Check MAIL_USERNAME and MAIL_PASSWORD are set
- Verify Gmail App Password is correct
- Check internet connectivity
- Review Flask logs for email errors

#### 2. Analytics Dashboard Not Loading
**Problem:** 404 error on analytics dashboard

**Solutions:**
- Ensure analytics blueprint is registered
- Check login system is working
- Verify user has admin privileges

#### 3. Form Validation Errors
**Problem:** Form fields showing validation errors

**Solutions:**
- Check all required fields are filled
- Verify specialties field has selections
- Ensure service type is selected

#### 4. State Page 404 Errors
**Problem:** State pages returning 404

**Solutions:**
- Check state data JSON files exist in `data/states/`
- Verify URL format: `/state/medical-billing-services-in-state-name`
- Check slugify function is working correctly

### Debug Mode
Enable debug mode for detailed error messages:
```python
# In run.py or environment
app.run(debug=True)
```

## Production Deployment

### 1. Security Configuration
```python
# Use strong secret key
SECRET_KEY = os.environ.get('SECRET_KEY')

# Disable debug mode
DEBUG = False

# Use secure email credentials
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
```

### 2. Database Considerations
For production, consider migrating from JSON storage to a proper database:
- PostgreSQL for relational data
- Redis for caching
- Separate analytics database

### 3. Web Server Configuration
Use a production WSGI server:
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 run:app
```

### 4. Monitoring Setup
- Set up log rotation for analytics data
- Monitor email delivery rates
- Track form submission patterns
- Set up alerts for system errors

## Maintenance

### Regular Tasks
- **Weekly:** Review analytics logs for insights
- **Monthly:** Clean up old analytics data
- **Quarterly:** Update dependencies
- **As needed:** Update state data JSON files

### Log Management
```bash
# View recent analytics data
tail -f logs/analytics_log.json

# Backup analytics data
cp logs/analytics_log.json logs/analytics_backup_$(date +%Y%m%d).json
```

### Updates and Patches
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Test after updates
python test_system.py
```

## Support and Resources

### Documentation
- Flask documentation: https://flask.palletsprojects.com/
- Flask-Mail documentation: https://flask-mail.readthedocs.io/
- Tailwind CSS documentation: https://tailwindcss.com/

### Contact
For deployment support or issues:
- Check the implementation summary: `IMPLEMENTATION_SUMMARY.md`
- Run the test script: `python test_system.py`
- Review Flask logs for specific error messages

### Quick Reference Commands
```bash
# Start development server
python run.py

# Run tests
python test_system.py

# View logs
tail -f logs/analytics_log.json

# Export analytics data
curl http://localhost:5000/analytics/export/csv
```

---

**Last Updated:** December 2024  
**Version:** 1.0.0  
**Status:** Production Ready