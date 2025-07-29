from flask import render_template, redirect, url_for, flash, request, jsonify, Response, current_app
from flask_login import login_required, current_user
from . import crm
from .models import Lead, Client, Activity, LeadStatus, ClientStatus, Priority
from .forms import LeadForm, ClientForm, ActivityForm, SearchForm
from ..auth.models import Permission
from ..auth.routes import require_permission
from datetime import datetime, timedelta
import csv
import io
from collections import Counter

@crm.route('/dashboard')
@login_required
@require_permission(Permission.CRM_VIEW)
def dashboard():
    """CRM dashboard with overview statistics"""
    try:
        # Get all leads and clients
        leads = Lead.get_all()
        clients = Client.get_all()
        activities = Activity.get_all()
        
        # Filter by user role
        if not current_user.is_manager():
            # Non-managers only see their own records
            leads = [l for l in leads if l.assigned_to == current_user.username]
            clients = [c for c in clients if c.assigned_to == current_user.username]
            activities = [a for a in activities if a.assigned_to == current_user.username]
        
        # Calculate statistics
        total_leads = len(leads)
        total_clients = len(clients)
        
        # Lead statistics
        lead_status_counts = Counter(lead.status.value for lead in leads)
        new_leads = lead_status_counts.get('new', 0)
        hot_leads = len([l for l in leads if l.priority.value in ['high', 'urgent']])
        
        # Client statistics  
        active_clients = len([c for c in clients if c.status == ClientStatus.ACTIVE])
        total_contract_value = sum(c.contract_value for c in clients if c.contract_value)
        
        # Recent activities
        recent_activities = sorted(activities, key=lambda a: a.created_at, reverse=True)[:10]
        
        # Upcoming follow-ups
        upcoming_followups = [
            l for l in leads 
            if l.follow_up_date and datetime.fromisoformat(l.follow_up_date) <= datetime.now() + timedelta(days=7)
        ]
        
        # Pipeline analysis
        pipeline_data = {}
        for status in LeadStatus:
            status_leads = [l for l in leads if l.status == status]
            pipeline_data[status.value] = {
                'count': len(status_leads),
                'value': sum(l.estimated_value for l in status_leads if l.estimated_value)
            }
        
        dashboard_stats = {
            'total_leads': total_leads,
            'total_clients': total_clients,
            'new_leads': new_leads,
            'hot_leads': hot_leads,
            'active_clients': active_clients,
            'total_contract_value': total_contract_value,
            'lead_status_counts': dict(lead_status_counts),
            'recent_activities': recent_activities,
            'upcoming_followups': upcoming_followups,
            'pipeline_data': pipeline_data
        }
        
        return render_template('crm/dashboard.html', stats=dashboard_stats)
        
    except Exception as e:
        current_app.logger.error(f"Error loading CRM dashboard: {str(e)}")
        flash('Error loading dashboard data', 'error')
        return render_template('crm/dashboard.html', stats={})

# Lead Management Routes
@crm.route('/leads')
@login_required
@require_permission(Permission.CRM_VIEW)
def leads():
    """List all leads with search and filtering"""
    form = SearchForm()
    leads = Lead.get_all()
    
    # Filter by user role
    if not current_user.is_manager():
        leads = [l for l in leads if l.assigned_to == current_user.username]
    
    # Apply search filters
    if form.validate_on_submit() and form.search_query.data:
        query = form.search_query.data.lower()
        search_type = form.search_type.data
        
        if search_type == 'name':
            leads = [l for l in leads if query in l.full_name.lower()]
        elif search_type == 'email':
            leads = [l for l in leads if query in l.email.lower()]
        elif search_type == 'company':
            leads = [l for l in leads if query in l.company.lower()]
        elif search_type == 'phone':
            leads = [l for l in leads if query in l.phone.lower()]
        else:  # all fields
            leads = [l for l in leads if (
                query in l.full_name.lower() or
                query in l.email.lower() or
                query in l.company.lower() or
                query in l.phone.lower()
            )]
    
    # Apply status filter
    if request.args.get('status'):
        status_filter = request.args.get('status')
        leads = [l for l in leads if l.status.value == status_filter]
        form.status_filter.data = status_filter
    
    # Apply specialty filter
    if request.args.get('specialty'):
        specialty_filter = request.args.get('specialty')
        leads = [l for l in leads if l.specialty == specialty_filter]
        form.specialty_filter.data = specialty_filter
    
    # Sort leads (newest first by default)
    leads.sort(key=lambda l: l.created_at, reverse=True)
    
    return render_template('crm/leads.html', leads=leads, form=form)

@crm.route('/leads/create', methods=['GET', 'POST'])
@login_required
@require_permission(Permission.CRM_CREATE)
def create_lead():
    """Create a new lead"""
    form = LeadForm()
    
    if form.validate_on_submit():
        lead = Lead(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            website=form.website.data,
            specialty=form.specialty.data,
            services_interested=form.services_interested.data,
            status=LeadStatus(form.status.data),
            priority=Priority(form.priority.data),
            source=form.source.data,
            assigned_to=form.assigned_to.data or current_user.username,
            follow_up_date=form.follow_up_date.data.isoformat() if form.follow_up_date.data else None,
            estimated_value=form.estimated_value.data or 0,
            probability=form.probability.data or 0,
            notes=form.notes.data
        )
        
        lead.save()
        
        # Create initial activity
        activity = Activity(
            type='note',
            subject='Lead Created',
            description=f'New lead created: {lead.full_name} from {lead.company}',
            related_to='lead',
            related_id=lead.id,
            assigned_to=lead.assigned_to,
            status='completed',
            created_by=current_user.username
        )
        activity.save()
        
        flash(f'Lead {lead.full_name} created successfully!', 'success')
        return redirect(url_for('crm.view_lead', lead_id=lead.id))
    
    return render_template('crm/create_lead.html', form=form)

@crm.route('/leads/<lead_id>')
@login_required
@require_permission(Permission.CRM_VIEW)
def view_lead(lead_id):
    """View lead details"""
    lead = Lead.get(lead_id)
    if not lead:
        flash('Lead not found.', 'error')
        return redirect(url_for('crm.leads'))
    
    # Check permissions
    if not current_user.is_manager() and lead.assigned_to != current_user.username:
        flash('You do not have permission to view this lead.', 'error')
        return redirect(url_for('crm.leads'))
    
    # Get related activities
    activities = Activity.get_by_related('lead', lead_id)
    activities.sort(key=lambda a: a.created_at, reverse=True)
    
    return render_template('crm/view_lead.html', lead=lead, activities=activities)

@crm.route('/leads/<lead_id>/edit', methods=['GET', 'POST'])
@login_required
@require_permission(Permission.CRM_EDIT)
def edit_lead(lead_id):
    """Edit lead details"""
    lead = Lead.get(lead_id)
    if not lead:
        flash('Lead not found.', 'error')
        return redirect(url_for('crm.leads'))
    
    # Check permissions
    if not current_user.is_manager() and lead.assigned_to != current_user.username:
        flash('You do not have permission to edit this lead.', 'error')
        return redirect(url_for('crm.leads'))
    
    form = LeadForm(obj=lead)
    
    if form.validate_on_submit():
        # Track status changes
        old_status = lead.status
        
        # Update lead data
        lead.first_name = form.first_name.data
        lead.last_name = form.last_name.data
        lead.email = form.email.data
        lead.phone = form.phone.data
        lead.company = form.company.data
        lead.website = form.website.data
        lead.specialty = form.specialty.data
        lead.services_interested = form.services_interested.data
        lead.status = LeadStatus(form.status.data)
        lead.priority = Priority(form.priority.data)
        lead.source = form.source.data
        lead.assigned_to = form.assigned_to.data
        lead.follow_up_date = form.follow_up_date.data.isoformat() if form.follow_up_date.data else None
        lead.estimated_value = form.estimated_value.data or 0
        lead.probability = form.probability.data or 0
        lead.notes = form.notes.data
        
        lead.save()
        
        # Create activity for status change
        if old_status != lead.status:
            activity = Activity(
                type='note',
                subject='Status Changed',
                description=f'Lead status changed from {old_status.value} to {lead.status.value}',
                related_to='lead',
                related_id=lead.id,
                assigned_to=lead.assigned_to,
                status='completed',
                created_by=current_user.username
            )
            activity.save()
        
        flash(f'Lead {lead.full_name} updated successfully!', 'success')
        return redirect(url_for('crm.view_lead', lead_id=lead.id))
    
    # Pre-populate form
    form.follow_up_date.data = datetime.fromisoformat(lead.follow_up_date).date() if lead.follow_up_date else None
    
    return render_template('crm/edit_lead.html', form=form, lead=lead)

@crm.route('/leads/<lead_id>/convert', methods=['POST'])
@login_required
@require_permission(Permission.CRM_EDIT)
def convert_lead(lead_id):
    """Convert lead to client"""
    lead = Lead.get(lead_id)
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    
    # Check permissions
    if not current_user.is_manager() and lead.assigned_to != current_user.username:
        return jsonify({'error': 'Permission denied'}), 403
    
    try:
        client = lead.convert_to_client()
        
        # Create activity
        activity = Activity(
            type='note',
            subject='Lead Converted',
            description=f'Lead converted to client: {client.full_name}',
            related_to='client',
            related_id=client.id,
            assigned_to=client.assigned_to,
            status='completed',
            created_by=current_user.username
        )
        activity.save()
        
        return jsonify({
            'message': f'Lead converted to client successfully!',
            'client_id': client.id
        })
        
    except Exception as e:
        current_app.logger.error(f"Error converting lead: {str(e)}")
        return jsonify({'error': 'Failed to convert lead'}), 500

@crm.route('/leads/<lead_id>/delete', methods=['POST'])
@login_required
@require_permission(Permission.CRM_DELETE)
def delete_lead(lead_id):
    """Delete a lead"""
    lead = Lead.get(lead_id)
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    
    # Check permissions
    if not current_user.is_manager() and lead.assigned_to != current_user.username:
        return jsonify({'error': 'Permission denied'}), 403
    
    if lead.delete():
        return jsonify({'message': f'Lead {lead.full_name} deleted successfully'})
    else:
        return jsonify({'error': 'Failed to delete lead'}), 500

# Client Management Routes
@crm.route('/clients')
@login_required
@require_permission(Permission.CRM_VIEW)
def clients():
    """List all clients"""
    clients = Client.get_all()
    
    # Filter by user role
    if not current_user.is_manager():
        clients = [c for c in clients if c.assigned_to == current_user.username]
    
    # Sort clients (newest first by default)
    clients.sort(key=lambda c: c.created_at, reverse=True)
    
    return render_template('crm/clients.html', clients=clients)

@crm.route('/clients/<client_id>')
@login_required
@require_permission(Permission.CRM_VIEW)
def view_client(client_id):
    """View client details"""
    client = Client.get(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('crm.clients'))
    
    # Check permissions
    if not current_user.is_manager() and client.assigned_to != current_user.username:
        flash('You do not have permission to view this client.', 'error')
        return redirect(url_for('crm.clients'))
    
    # Get related activities
    activities = Activity.get_by_related('client', client_id)
    activities.sort(key=lambda a: a.created_at, reverse=True)
    
    return render_template('crm/view_client.html', client=client, activities=activities)

@crm.route('/clients/<client_id>/edit', methods=['GET', 'POST'])
@login_required
@require_permission(Permission.CRM_EDIT)
def edit_client(client_id):
    """Edit client details"""
    client = Client.get(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('crm.clients'))
    
    # Check permissions
    if not current_user.is_manager() and client.assigned_to != current_user.username:
        flash('You do not have permission to edit this client.', 'error')
        return redirect(url_for('crm.clients'))
    
    form = ClientForm(obj=client)
    
    if form.validate_on_submit():
        # Update client data
        client.first_name = form.first_name.data
        client.last_name = form.last_name.data
        client.email = form.email.data
        client.phone = form.phone.data
        client.company = form.company.data
        client.website = form.website.data
        client.specialty = form.specialty.data
        client.services = form.services.data
        client.status = ClientStatus(form.status.data)
        client.assigned_to = form.assigned_to.data
        client.contract_value = form.contract_value.data or 0
        client.contract_start_date = form.contract_start_date.data.isoformat() if form.contract_start_date.data else None
        client.contract_end_date = form.contract_end_date.data.isoformat() if form.contract_end_date.data else None
        client.billing_contact = form.billing_contact.data
        client.billing_email = form.billing_email.data
        client.billing_address = form.billing_address.data
        client.notes = form.notes.data
        
        client.save()
        
        flash(f'Client {client.full_name} updated successfully!', 'success')
        return redirect(url_for('crm.view_client', client_id=client.id))
    
    # Pre-populate form
    if client.contract_start_date:
        form.contract_start_date.data = datetime.fromisoformat(client.contract_start_date).date()
    if client.contract_end_date:
        form.contract_end_date.data = datetime.fromisoformat(client.contract_end_date).date()
    
    return render_template('crm/edit_client.html', form=form, client=client)

# Activity Management Routes
@crm.route('/activities')
@login_required
@require_permission(Permission.CRM_VIEW)
def activities():
    """List all activities"""
    activities = Activity.get_all()
    
    # Filter by user role
    if not current_user.is_manager():
        activities = [a for a in activities if a.assigned_to == current_user.username]
    
    # Sort activities (newest first)
    activities.sort(key=lambda a: a.created_at, reverse=True)
    
    return render_template('crm/activities.html', activities=activities)

@crm.route('/activities/create/<related_to>/<related_id>', methods=['GET', 'POST'])
@login_required
@require_permission(Permission.CRM_CREATE)
def create_activity(related_to, related_id):
    """Create a new activity"""
    form = ActivityForm()
    
    # Verify the related object exists
    if related_to == 'lead':
        related_obj = Lead.get(related_id)
    elif related_to == 'client':
        related_obj = Client.get(related_id)
    else:
        flash('Invalid relation type.', 'error')
        return redirect(url_for('crm.dashboard'))
    
    if not related_obj:
        flash(f'{related_to.title()} not found.', 'error')
        return redirect(url_for('crm.dashboard'))
    
    if form.validate_on_submit():
        activity = Activity(
            type=form.type.data,
            subject=form.subject.data,
            description=form.description.data,
            related_to=related_to,
            related_id=related_id,
            assigned_to=form.assigned_to.data or current_user.username,
            status=form.status.data,
            due_date=form.due_date.data.isoformat() if form.due_date.data else None,
            created_by=current_user.username
        )
        
        activity.save()
        
        flash('Activity created successfully!', 'success')
        
        if related_to == 'lead':
            return redirect(url_for('crm.view_lead', lead_id=related_id))
        else:
            return redirect(url_for('crm.view_client', client_id=related_id))
    
    return render_template('crm/create_activity.html', form=form, related_to=related_to, related_obj=related_obj)

# Export Routes
@crm.route('/leads/export')
@login_required
@require_permission(Permission.CRM_EXPORT)
def export_leads():
    """Export leads to CSV"""
    leads = Lead.get_all()
    
    # Filter by user role
    if not current_user.is_manager():
        leads = [l for l in leads if l.assigned_to == current_user.username]
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Company', 
        'Website', 'Specialty', 'Services Interested', 'Status', 'Priority',
        'Source', 'Assigned To', 'Follow-up Date', 'Estimated Value',
        'Probability', 'Created At', 'Notes'
    ])
    
    # Write data
    for lead in leads:
        writer.writerow([
            lead.id, lead.first_name, lead.last_name, lead.email, lead.phone,
            lead.company, lead.website, lead.specialty, 
            ', '.join(lead.services_interested), lead.status.value, lead.priority.value,
            lead.source, lead.assigned_to, lead.follow_up_date, lead.estimated_value,
            lead.probability, lead.created_at, lead.notes
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=leads_export.csv'}
    )

@crm.route('/clients/export')
@login_required
@require_permission(Permission.CRM_EXPORT)
def export_clients():
    """Export clients to CSV"""
    clients = Client.get_all()
    
    # Filter by user role
    if not current_user.is_manager():
        clients = [c for c in clients if c.assigned_to == current_user.username]
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Company',
        'Website', 'Specialty', 'Services', 'Status', 'Assigned To',
        'Contract Value', 'Contract Start', 'Contract End', 'Billing Contact',
        'Billing Email', 'Created At', 'Notes'
    ])
    
    # Write data
    for client in clients:
        writer.writerow([
            client.id, client.first_name, client.last_name, client.email, client.phone,
            client.company, client.website, client.specialty, ', '.join(client.services),
            client.status.value, client.assigned_to, client.contract_value,
            client.contract_start_date, client.contract_end_date, client.billing_contact,
            client.billing_email, client.created_at, client.notes
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=clients_export.csv'}
    )
