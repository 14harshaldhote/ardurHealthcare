import json
import os
from typing import Any, Dict, List
from datetime import datetime

def ensure_directory_exists(filepath: str) -> None:
    """Ensure the directory for a file exists, create if it doesn't"""
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_json(filepath: str) -> Dict[str, Any]:
    """Read data from a JSON file"""
    ensure_directory_exists(filepath)
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_json(filepath: str, data: Dict[str, Any]) -> None:
    """Write data to a JSON file"""
    ensure_directory_exists(filepath)
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4, default=str)
    except IOError as e:
        print(f"Error writing to {filepath}: {e}")

def append_to_json(filepath: str, new_data: Dict[str, Any]) -> None:
    """Appends new data to a JSON file"""
    data = read_json(filepath)
    if isinstance(data, dict):
        data.update(new_data)
        write_json(filepath, data)

def save_contact_message(filepath: str, name: str, email: str, subject: str, message: str) -> None:
    """Save a contact form submission"""
    contacts = read_json(filepath)
    if 'messages' not in contacts:
        contacts['messages'] = []
    
    contacts['messages'].append({
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
        'timestamp': datetime.now().isoformat()
    })
    write_json(filepath, contacts)