from flask import render_template, jsonify, request, current_app
from flask_login import login_required
from . import analytics
from ..auth.models import Permission
from ..auth.routes import require_permission
import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict


@analytics.route('/dashboard')
@login_required
@require_permission(Permission.ANALYTICS_VIEW)
def dashboard():
    """Analytics dashboard showing form submission data"""
    try:
        analytics_data = load_analytics_data()

        # Process data for dashboard
        total_submissions = len(analytics_data)

        # Get submissions by state
        states = Counter(entry['state'] for entry in analytics_data)

        # Get submissions by service type
        service_types = Counter(entry['service_type'] for entry in analytics_data if entry['service_type'])

        # Get submissions by specialty (flatten the lists)
        all_specialties = []
        for entry in analytics_data:
            if entry['specialties']:
                all_specialties.extend(entry['specialties'])
        specialties = Counter(all_specialties)

        # Get recent submissions (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_submissions = [
            entry for entry in analytics_data
            if datetime.fromisoformat(entry['timestamp']) > thirty_days_ago
        ]

        # Daily submissions for the last 30 days
        daily_submissions = defaultdict(int)
        for entry in recent_submissions:
            date = datetime.fromisoformat(entry['timestamp']).date()
            daily_submissions[date.isoformat()] += 1

        dashboard_data = {
            'total_submissions': total_submissions,
            'recent_submissions': len(recent_submissions),
            'top_states': dict(states.most_common(10)),
            'top_services': dict(service_types.most_common(10)),
            'top_specialties': dict(specialties.most_common(10)),
            'daily_submissions': dict(daily_submissions),
            'latest_submissions': analytics_data[-10:] if analytics_data else []
        }

        return render_template('analytics/dashboard.html', data=dashboard_data)

    except Exception as e:
        current_app.logger.error(f"Error loading analytics dashboard: {str(e)}")
        return render_template('analytics/dashboard.html', data={
            'error': 'Unable to load analytics data'
        })


@analytics.route('/api/data')
@login_required
@require_permission(Permission.ANALYTICS_VIEW)
def api_data():
    """API endpoint for analytics data"""
    try:
        analytics_data = load_analytics_data()

        # Filter by date range if provided
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if start_date:
            start_date = datetime.fromisoformat(start_date)
            analytics_data = [
                entry for entry in analytics_data
                if datetime.fromisoformat(entry['timestamp']) >= start_date
            ]

        if end_date:
            end_date = datetime.fromisoformat(end_date)
            analytics_data = [
                entry for entry in analytics_data
                if datetime.fromisoformat(entry['timestamp']) <= end_date
            ]

        # Filter by state if provided
        state_filter = request.args.get('state')
        if state_filter:
            analytics_data = [
                entry for entry in analytics_data
                if entry['state'].lower() == state_filter.lower()
            ]

        # Filter by service type if provided
        service_filter = request.args.get('service_type')
        if service_filter:
            analytics_data = [
                entry for entry in analytics_data
                if entry['service_type'] and entry['service_type'].lower() == service_filter.lower()
            ]

        return jsonify({
            'success': True,
            'data': analytics_data,
            'count': len(analytics_data)
        })

    except Exception as e:
        current_app.logger.error(f"Error fetching analytics data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Unable to fetch analytics data'
        }), 500


@analytics.route('/reports/state-summary')
@login_required
@require_permission(Permission.ANALYTICS_VIEW)
def state_summary():
    """Generate state-wise summary report"""
    try:
        analytics_data = load_analytics_data()

        # Group by state
        state_data = {}
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        for entry in analytics_data:
            state = entry['state']

            # Initialize state data if not exists
            if state not in state_data:
                state_data[state] = {
                    'total': 0,
                    'services': {},
                    'specialties': {},
                    'recent': 0
                }

            # Update counters
            state_data[state]['total'] += 1

            if entry['service_type']:
                service = entry['service_type']
                state_data[state]['services'][service] = state_data[state]['services'].get(service, 0) + 1

            if entry['specialties']:
                for specialty in entry['specialties']:
                    state_data[state]['specialties'][specialty] = state_data[state]['specialties'].get(specialty, 0) + 1

            if datetime.fromisoformat(entry['timestamp']) > thirty_days_ago:
                state_data[state]['recent'] += 1

        return render_template('analytics/state_summary.html', state_data=state_data)

    except Exception as e:
        current_app.logger.error(f"Error generating state summary: {str(e)}")
        return render_template('analytics/state_summary.html', state_data={}, error=str(e))


def load_analytics_data():
    """Load analytics data from JSON file"""
    try:
        log_file = os.path.join(current_app.root_path, '..', 'logs', 'analytics_log.json')

        if not os.path.exists(log_file):
            return []

        with open(log_file, 'r') as f:
            data = json.load(f)

        # Sort by timestamp
        data.sort(key=lambda x: x['timestamp'])

        return data

    except Exception as e:
        current_app.logger.error(f"Error loading analytics data: {str(e)}")
        return []


@analytics.route('/export/csv')
@login_required
@require_permission(Permission.ANALYTICS_EXPORT)
def export_csv():
    """Export analytics data as CSV"""
    try:
        from flask import Response
        import csv
        from io import StringIO

        analytics_data = load_analytics_data()

        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['Timestamp', 'State', 'Service Type', 'Specialties', 'Source'])

        # Write data
        for entry in analytics_data:
            specialties_str = ', '.join(entry['specialties']) if entry['specialties'] else ''
            writer.writerow([
                entry['timestamp'],
                entry['state'],
                entry['service_type'] or '',
                specialties_str,
                entry['source']
            ])

        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=analytics_data.csv'}
        )

    except Exception as e:
        current_app.logger.error(f"Error exporting CSV: {str(e)}")
        return jsonify({'error': 'Unable to export data'}), 500
