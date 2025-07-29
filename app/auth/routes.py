from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SignupForm, LoginForm, AdminSignupForm, EditUserForm, ChangePasswordForm
from .models import User, UserRole, Permission
from ..utils.file_ops import read_json, write_json
from functools import wraps

auth = Blueprint('auth', __name__)

# Decorator for role-based access control
def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('auth.login'))
            
            if not current_user.has_permission(permission):
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('main.home'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = SignupForm()
    if form.validate_on_submit():
        users = read_json(current_app.config['USERS_FILE'])
        if form.username.data in users:
            flash('Username already taken. Please choose another.', 'error')
            return render_template('signup.html', form=form)
        
        # Create new user with client role by default
        User.create(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=UserRole.CLIENT
        )
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        users = read_json(current_app.config['USERS_FILE'])
        user_data = users.get(form.username.data)
        
        if user_data and check_password_hash(user_data['password_hash'], form.password.data):
            user = User.get(form.username.data)
            if user and user.is_active:
                login_user(user)
                flash(f'Welcome back, {user.username}!', 'success')
                
                # Redirect based on role
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                elif user.is_admin():
                    return redirect(url_for('auth.admin_dashboard'))
                elif user.can_access_crm():
                    return redirect(url_for('crm.dashboard'))
                else:
                    return redirect(url_for('main.home'))
            else:
                flash('Your account has been deactivated. Please contact support.', 'error')
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Admin routes for user management
@auth.route('/admin/dashboard')
@login_required
@require_permission(Permission.USER_VIEW)
def admin_dashboard():
    """Admin dashboard for user management"""
    users = User.get_all()
    return render_template('admin/dashboard.html', users=users)

@auth.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
@require_permission(Permission.USER_CREATE)
def create_user():
    """Create a new user (admin only)"""
    form = AdminSignupForm()
    if form.validate_on_submit():
        users = read_json(current_app.config['USERS_FILE'])
        if form.username.data in users:
            flash('Username already taken. Please choose another.', 'error')
            return render_template('admin/create_user.html', form=form)
        
        # Create user profile
        profile = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'phone': form.phone.data,
            'company': form.company.data,
            'notes': form.notes.data
        }
        
        User.create(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=UserRole(form.role.data),
            profile=profile
        )
        
        flash(f'User {form.username.data} created successfully!', 'success')
        return redirect(url_for('auth.admin_dashboard'))
    
    return render_template('admin/create_user.html', form=form)

@auth.route('/admin/users/<username>/edit', methods=['GET', 'POST'])
@login_required
@require_permission(Permission.USER_EDIT)
def edit_user(username):
    """Edit user details (admin/manager only)"""
    user = User.get(username)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.admin_dashboard'))
    
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        # Update user data
        user.email = form.email.data
        user.role = UserRole(form.role.data)
        user.is_active = form.is_active.data
        
        # Update profile
        user.profile.update({
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'phone': form.phone.data,
            'company': form.company.data,
            'notes': form.notes.data
        })
        
        user.save()
        flash(f'User {username} updated successfully!', 'success')
        return redirect(url_for('auth.admin_dashboard'))
    
    # Pre-populate form with user data
    form.email.data = user.email
    form.role.data = user.role.value
    form.is_active.data = user.is_active
    if user.profile:
        form.first_name.data = user.profile.get('first_name', '')
        form.last_name.data = user.profile.get('last_name', '')
        form.phone.data = user.profile.get('phone', '')
        form.company.data = user.profile.get('company', '')
        form.notes.data = user.profile.get('notes', '')
    
    return render_template('admin/edit_user.html', form=form, user=user)

@auth.route('/admin/users/<username>/delete', methods=['POST'])
@login_required
@require_permission(Permission.USER_DELETE)
def delete_user(username):
    """Delete a user (admin only)"""
    if username == current_user.username:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    user = User.get(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.delete():
        return jsonify({'message': f'User {username} deleted successfully'})
    else:
        return jsonify({'error': 'Failed to delete user'}), 500

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    form = EditUserForm(obj=current_user)
    
    # Remove role field for non-admin users
    if not current_user.is_admin():
        delattr(form, 'role')
        delattr(form, 'is_active')
    
    if form.validate_on_submit():
        current_user.email = form.email.data
        
        # Only admins can change roles and status
        if current_user.is_admin():
            current_user.role = UserRole(form.role.data)
            current_user.is_active = form.is_active.data
        
        # Update profile
        current_user.profile.update({
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'phone': form.phone.data,
            'company': form.company.data,
        })
        
        current_user.save()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    # Pre-populate form
    form.email.data = current_user.email
    if hasattr(form, 'role'):
        form.role.data = current_user.role.value
        form.is_active.data = current_user.is_active
    
    if current_user.profile:
        form.first_name.data = current_user.profile.get('first_name', '')
        form.last_name.data = current_user.profile.get('last_name', '')
        form.phone.data = current_user.profile.get('phone', '')
        form.company.data = current_user.profile.get('company', '')
        form.notes.data = current_user.profile.get('notes', '')
    
    return render_template('profile.html', form=form, user=current_user)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        users = read_json(current_app.config['USERS_FILE'])
        user_data = users.get(current_user.username)
        
        if user_data and check_password_hash(user_data['password_hash'], form.current_password.data):
            if form.new_password.data == form.confirm_password.data:
                users[current_user.username]['password_hash'] = generate_password_hash(form.new_password.data)
                write_json(current_app.config['USERS_FILE'], users)
                flash('Password changed successfully!', 'success')
                return redirect(url_for('auth.profile'))
            else:
                flash('New passwords do not match.', 'error')
        else:
            flash('Current password is incorrect.', 'error')
    
    return render_template('change_password.html', form=form)
