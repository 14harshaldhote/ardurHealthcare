from datetime import datetime
from enum import Enum
from flask import current_app
from ..utils.file_ops import read_json, write_json
import uuid
import json

class LeadStatus(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    ON_HOLD = "on_hold"

class ClientStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"

class ServiceType(Enum):
    MEDICAL_BILLING = "medical_billing"
    ELIGIBILITY_VERIFICATION = "eligibility_verification"
    PRIOR_AUTHORIZATION = "prior_authorization"
    PROVIDER_CREDENTIALING = "provider_credentialing"
    CHARGE_ENTRY = "charge_entry"
    MEDICAL_CODING = "medical_coding"
    CLAIM_SUBMISSION = "claim_submission"
    PAYMENT_POSTING = "payment_posting"
    DENIAL_MANAGEMENT = "denial_management"
    AR_MANAGEMENT = "ar_management"
    FULL_RCM = "full_rcm"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Lead:
    def __init__(self, id=None, first_name="", last_name="", email="", phone="", company="", 
                 website="", specialty="", services_interested=None, status=LeadStatus.NEW,
                 priority=Priority.MEDIUM, source="", notes="", assigned_to="",
                 created_at=None, updated_at=None, follow_up_date=None, 
                 estimated_value=0, probability=0):
        self.id = id or str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.company = company
        self.website = website
        self.specialty = specialty
        self.services_interested = services_interested or []
        self.status = status if isinstance(status, LeadStatus) else LeadStatus(status)
        self.priority = priority if isinstance(priority, Priority) else Priority(priority)
        self.source = source
        self.notes = notes
        self.assigned_to = assigned_to
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()
        self.follow_up_date = follow_up_date
        self.estimated_value = estimated_value
        self.probability = probability

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'website': self.website,
            'specialty': self.specialty,
            'services_interested': self.services_interested,
            'status': self.status.value,
            'priority': self.priority.value,
            'source': self.source,
            'notes': self.notes,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'follow_up_date': self.follow_up_date,
            'estimated_value': self.estimated_value,
            'probability': self.probability
        }

    @staticmethod
    def from_dict(data):
        return Lead(**data)

    def save(self):
        self.updated_at = datetime.utcnow().isoformat()
        leads = read_json(current_app.config['LEADS_FILE'])
        leads[self.id] = self.to_dict()
        write_json(current_app.config['LEADS_FILE'], leads)

    @staticmethod
    def get(lead_id):
        leads = read_json(current_app.config['LEADS_FILE'])
        lead_data = leads.get(lead_id)
        if lead_data:
            return Lead.from_dict(lead_data)
        return None

    @staticmethod
    def get_all():
        leads = read_json(current_app.config['LEADS_FILE'])
        return [Lead.from_dict(data) for data in leads.values()]

    def delete(self):
        leads = read_json(current_app.config['LEADS_FILE'])
        if self.id in leads:
            del leads[self.id]
            write_json(current_app.config['LEADS_FILE'], leads)
            return True
        return False

    def convert_to_client(self):
        """Convert lead to client"""
        client = Client(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            company=self.company,
            website=self.website,
            specialty=self.specialty,
            services=self.services_interested,
            status=ClientStatus.ACTIVE,
            assigned_to=self.assigned_to,
            notes=f"Converted from lead. Original notes: {self.notes}",
            contract_value=self.estimated_value
        )
        client.save()
        
        # Update lead status
        self.status = LeadStatus.CLOSED_WON
        self.save()
        
        return client

class Client:
    def __init__(self, id=None, first_name="", last_name="", email="", phone="", company="",
                 website="", specialty="", services=None, status=ClientStatus.ACTIVE,
                 assigned_to="", notes="", contract_value=0, contract_start_date=None,
                 contract_end_date=None, billing_contact="", billing_email="", 
                 billing_address="", created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.company = company
        self.website = website
        self.specialty = specialty
        self.services = services or []
        self.status = status if isinstance(status, ClientStatus) else ClientStatus(status)
        self.assigned_to = assigned_to
        self.notes = notes
        self.contract_value = contract_value
        self.contract_start_date = contract_start_date
        self.contract_end_date = contract_end_date
        self.billing_contact = billing_contact
        self.billing_email = billing_email
        self.billing_address = billing_address
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'website': self.website,
            'specialty': self.specialty,
            'services': self.services,
            'status': self.status.value,
            'assigned_to': self.assigned_to,
            'notes': self.notes,
            'contract_value': self.contract_value,
            'contract_start_date': self.contract_start_date,
            'contract_end_date': self.contract_end_date,
            'billing_contact': self.billing_contact,
            'billing_email': self.billing_email,
            'billing_address': self.billing_address,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def from_dict(data):
        return Client(**data)

    def save(self):
        self.updated_at = datetime.utcnow().isoformat()
        clients = read_json(current_app.config['CLIENTS_FILE'])
        clients[self.id] = self.to_dict()
        write_json(current_app.config['CLIENTS_FILE'], clients)

    @staticmethod
    def get(client_id):
        clients = read_json(current_app.config['CLIENTS_FILE'])
        client_data = clients.get(client_id)
        if client_data:
            return Client.from_dict(client_data)
        return None

    @staticmethod
    def get_all():
        clients = read_json(current_app.config['CLIENTS_FILE'])
        return [Client.from_dict(data) for data in clients.values()]

    def delete(self):
        clients = read_json(current_app.config['CLIENTS_FILE'])
        if self.id in clients:
            del clients[self.id]
            write_json(current_app.config['CLIENTS_FILE'], clients)
            return True
        return False

class Activity:
    def __init__(self, id=None, type="", subject="", description="", related_to="",
                 related_id="", assigned_to="", status="pending", due_date=None,
                 completed_date=None, created_at=None, created_by=""):
        self.id = id or str(uuid.uuid4())
        self.type = type  # call, email, meeting, task, note
        self.subject = subject
        self.description = description
        self.related_to = related_to  # lead, client
        self.related_id = related_id
        self.assigned_to = assigned_to
        self.status = status  # pending, completed, cancelled
        self.due_date = due_date
        self.completed_date = completed_date
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.created_by = created_by

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'subject': self.subject,
            'description': self.description,
            'related_to': self.related_to,
            'related_id': self.related_id,
            'assigned_to': self.assigned_to,
            'status': self.status,
            'due_date': self.due_date,
            'completed_date': self.completed_date,
            'created_at': self.created_at,
            'created_by': self.created_by
        }

    @staticmethod
    def from_dict(data):
        return Activity(**data)

    def save(self):
        activities = read_json(current_app.config['ACTIVITIES_FILE'])
        activities[self.id] = self.to_dict()
        write_json(current_app.config['ACTIVITIES_FILE'], activities)

    @staticmethod
    def get(activity_id):
        activities = read_json(current_app.config['ACTIVITIES_FILE'])
        activity_data = activities.get(activity_id)
        if activity_data:
            return Activity.from_dict(activity_data)
        return None

    @staticmethod
    def get_all():
        activities = read_json(current_app.config['ACTIVITIES_FILE'])
        return [Activity.from_dict(data) for data in activities.values()]

    @staticmethod
    def get_by_related(related_to, related_id):
        """Get activities related to a specific lead or client"""
        activities = read_json(current_app.config['ACTIVITIES_FILE'])
        return [
            Activity.from_dict(data) 
            for data in activities.values() 
            if data.get('related_to') == related_to and data.get('related_id') == related_id
        ]

    def delete(self):
        activities = read_json(current_app.config['ACTIVITIES_FILE'])
        if self.id in activities:
            del activities[self.id]
            write_json(current_app.config['ACTIVITIES_FILE'], activities)
            return True
        return False
