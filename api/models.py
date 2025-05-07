"""
This module contains functions to simulate database operations.
In a real application, these would interact with a database.
"""
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Mock data for demonstrating insurance API functionality
# Note: In a real application, this would come from a database

# Members data for authentication and identification
members_data = [
    {
        'id': 1, 
        'member_id': 'MEM12345',
        'first_name': 'John', 
        'last_name': 'Doe', 
        'dob': '01/15/1985',
        'zip_code': '78745',
        'email': 'john.doe@example.com',
        'phone': '555-123-1234',
        'carrier': 'Ambetter',
        'plan_id': 1
    },
    {
        'id': 2, 
        'member_id': 'MEM67890',
        'first_name': 'Jane', 
        'last_name': 'Smith', 
        'dob': '05/20/1990',
        'zip_code': '33130',
        'email': 'jane.smith@example.com',
        'phone': '555-456-5678',
        'carrier': 'Oscar Health',
        'plan_id': 2
    },
    {
        'id': 3, 
        'member_id': 'MEM24680',
        'first_name': 'Robert', 
        'last_name': 'Johnson', 
        'dob': '11/30/1975',
        'zip_code': '90210',
        'email': 'robert.johnson@example.com',
        'phone': '555-789-9012',
        'carrier': 'Blue Cross Blue Shield',
        'plan_id': 3
    },
    {
        'id': 4, 
        'member_id': 'MEM13579',
        'first_name': 'Maria', 
        'last_name': 'Garcia', 
        'dob': '07/12/1988',
        'zip_code': '10001',
        'email': 'maria.garcia@example.com',
        'phone': '555-321-3456',
        'carrier': 'Aetna',
        'plan_id': 4
    },
    {
        'id': 5, 
        'member_id': 'MEM97531',
        'first_name': 'Carlos', 
        'last_name': 'Rodriguez', 
        'dob': '03/25/1992',
        'zip_code': '60601',
        'email': 'carlos.rodriguez@example.com',
        'phone': '555-654-7890',
        'carrier': 'Cigna',
        'plan_id': 5
    }
]

# Insurance carriers data with payment portals
carriers_data = [
    {
        'id': 1,
        'name': 'Ambetter',
        'payment_portal': 'https://ambetter.paymentportal.com',
        'payment_phone': '1-800-123-4567',
        'provider_directory': 'https://ambetter.providerdirectory.com',
        'customer_service': '1-888-123-4567',
        'spanish_support': True
    },
    {
        'id': 2,
        'name': 'Oscar Health',
        'payment_portal': 'https://oscar.paymentportal.com',
        'payment_phone': '1-800-234-5678',
        'provider_directory': 'https://oscar.providerdirectory.com',
        'customer_service': '1-888-234-5678',
        'spanish_support': True
    },
    {
        'id': 3,
        'name': 'Blue Cross Blue Shield',
        'payment_portal': 'https://bcbs.paymentportal.com',
        'payment_phone': '1-800-345-6789',
        'provider_directory': 'https://bcbs.providerdirectory.com',
        'customer_service': '1-888-345-6789',
        'spanish_support': True
    },
    {
        'id': 4,
        'name': 'Aetna',
        'payment_portal': 'https://aetna.paymentportal.com',
        'payment_phone': '1-800-456-7890',
        'provider_directory': 'https://aetna.providerdirectory.com',
        'customer_service': '1-888-456-7890',
        'spanish_support': False
    },
    {
        'id': 5,
        'name': 'Cigna',
        'payment_portal': 'https://cigna.paymentportal.com',
        'payment_phone': '1-800-567-8901',
        'provider_directory': 'https://cigna.providerdirectory.com',
        'customer_service': '1-888-567-8901',
        'spanish_support': True
    }
]

# Insurance plans data
plans_data = [
    {
        'id': 1,
        'carrier_id': 1,
        'name': 'Ambetter SecureCare Bronze 2025',
        'type': 'Bronze',
        'deductible': 8000,
        'out_of_pocket_max': 9000,
        'primary_care_copay': 40,
        'specialist_copay': 80,
        'emergency_copay': 500,
        'urgent_care_copay': 75,
        'generic_drug_copay': 25,
        'covers_dental': False,
        'covers_vision': False,
        'covers_mental_health': True,
        'sbc_url': 'https://ambetter.com/sbc/bronze2025.pdf'
    },
    {
        'id': 2,
        'carrier_id': 2,
        'name': 'Oscar Secure Silver 2025',
        'type': 'Silver',
        'deductible': 5000,
        'out_of_pocket_max': 7000,
        'primary_care_copay': 30,
        'specialist_copay': 60,
        'emergency_copay': 350,
        'urgent_care_copay': 50,
        'generic_drug_copay': 15,
        'covers_dental': False,
        'covers_vision': True,
        'covers_mental_health': True,
        'sbc_url': 'https://oscar.com/sbc/silver2025.pdf'
    },
    {
        'id': 3,
        'carrier_id': 3,
        'name': 'Blue Cross PPO Gold 2025',
        'type': 'Gold',
        'deductible': 2500,
        'out_of_pocket_max': 5000,
        'primary_care_copay': 20,
        'specialist_copay': 40,
        'emergency_copay': 250,
        'urgent_care_copay': 30,
        'generic_drug_copay': 10,
        'covers_dental': True,
        'covers_vision': True,
        'covers_mental_health': True,
        'sbc_url': 'https://bcbs.com/sbc/gold2025.pdf'
    },
    {
        'id': 4,
        'carrier_id': 4,
        'name': 'Aetna Premium Platinum 2025',
        'type': 'Platinum',
        'deductible': 0,
        'out_of_pocket_max': 3000,
        'primary_care_copay': 15,
        'specialist_copay': 30,
        'emergency_copay': 150,
        'urgent_care_copay': 25,
        'generic_drug_copay': 5,
        'covers_dental': True,
        'covers_vision': True,
        'covers_mental_health': True,
        'sbc_url': 'https://aetna.com/sbc/platinum2025.pdf'
    },
    {
        'id': 5,
        'carrier_id': 5,
        'name': 'Cigna Value Bronze 2025',
        'type': 'Bronze',
        'deductible': 7500,
        'out_of_pocket_max': 8500,
        'primary_care_copay': 35,
        'specialist_copay': 75,
        'emergency_copay': 450,
        'urgent_care_copay': 65,
        'generic_drug_copay': 20,
        'covers_dental': False,
        'covers_vision': False,
        'covers_mental_health': True,
        'sbc_url': 'https://cigna.com/sbc/bronze2025.pdf'
    }
]

# Provider network data
providers_data = [
    {
        'id': 1,
        'name': 'Dr. Sarah Johnson',
        'specialty': 'Primary Care',
        'location': 'Austin, TX',
        'zip_code': '78745',
        'accepting_new_patients': True,
        'languages': ['English', 'Spanish'],
        'carrier_networks': [1, 2, 3]  # IDs of carriers in whose network this doctor is
    },
    {
        'id': 2,
        'name': 'Dr. Michael Chen',
        'specialty': 'Cardiology',
        'location': 'Miami, FL',
        'zip_code': '33130',
        'accepting_new_patients': True,
        'languages': ['English', 'Mandarin'],
        'carrier_networks': [2, 3, 5]
    },
    {
        'id': 3,
        'name': 'Dr. Lisa Garcia',
        'specialty': 'Pediatrics',
        'location': 'Beverly Hills, CA',
        'zip_code': '90210',
        'accepting_new_patients': False,
        'languages': ['English', 'Spanish'],
        'carrier_networks': [1, 3, 4, 5]
    },
    {
        'id': 4,
        'name': 'Dr. James Wilson',
        'specialty': 'Orthopedics',
        'location': 'New York, NY',
        'zip_code': '10001',
        'accepting_new_patients': True,
        'languages': ['English'],
        'carrier_networks': [3, 4]
    },
    {
        'id': 5,
        'name': 'Dr. Maria Rodriguez',
        'specialty': 'Dermatology',
        'location': 'Chicago, IL',
        'zip_code': '60601',
        'accepting_new_patients': True,
        'languages': ['English', 'Spanish'],
        'carrier_networks': [1, 2, 4, 5]
    }
]

def authenticate_member(dob=None, zip_code=None, member_id=None):
    """
    Authenticate a member using either DOB + ZIP code or Member ID
    
    Args:
        dob (str, optional): Date of birth in MM/DD/YYYY format
        zip_code (str, optional): ZIP code
        member_id (str, optional): Member ID
        
    Returns:
        dict: Member data if authenticated, None otherwise
    """
    logger.debug(f"Authenticating member with DOB: {dob}, ZIP: {zip_code}, Member ID: {member_id}")
    
    if member_id:
        # Authenticate by member ID
        for member in members_data:
            if member['member_id'] == member_id:
                return member
    elif dob and zip_code:
        # Authenticate by DOB and ZIP
        for member in members_data:
            if member['dob'] == dob and member['zip_code'] == zip_code:
                return member
    
    return None

def get_carrier(carrier_id):
    """
    Get carrier information by ID
    
    Args:
        carrier_id (int): The ID of the carrier
        
    Returns:
        dict: Carrier data if found, None otherwise
    """
    logger.debug(f"Fetching carrier with ID {carrier_id}")
    for carrier in carriers_data:
        if carrier['id'] == carrier_id:
            return carrier
    return None

def get_carrier_by_name(name):
    """
    Get carrier information by name
    
    Args:
        name (str): The name of the carrier
        
    Returns:
        dict: Carrier data if found, None otherwise
    """
    logger.debug(f"Fetching carrier with name {name}")
    for carrier in carriers_data:
        if carrier['name'].lower() == name.lower():
            return carrier
    return None

def get_plan(plan_id):
    """
    Get plan information by ID
    
    Args:
        plan_id (int): The ID of the plan
        
    Returns:
        dict: Plan data if found, None otherwise
    """
    logger.debug(f"Fetching plan with ID {plan_id}")
    for plan in plans_data:
        if plan['id'] == plan_id:
            return plan
    return None

def get_member_plan(member_id):
    """
    Get a member's plan
    
    Args:
        member_id (int): The ID of the member
        
    Returns:
        dict: Plan data if found, None otherwise
    """
    logger.debug(f"Fetching plan for member with ID {member_id}")
    member = next((m for m in members_data if m['id'] == member_id), None)
    if member:
        return get_plan(member['plan_id'])
    return None

def get_providers(zip_code=None, specialty=None, carrier_id=None, limit=10):
    """
    Get providers based on filters
    
    Args:
        zip_code (str, optional): Provider ZIP code
        specialty (str, optional): Provider specialty
        carrier_id (int, optional): Carrier ID to filter providers in that network
        limit (int): Maximum number of providers to return
        
    Returns:
        list: List of provider dictionaries
    """
    logger.debug(f"Fetching providers with ZIP: {zip_code}, Specialty: {specialty}, Carrier ID: {carrier_id}")
    
    filtered_providers = providers_data
    
    if zip_code:
        filtered_providers = [p for p in filtered_providers if p['zip_code'] == zip_code]
    
    if specialty:
        filtered_providers = [p for p in filtered_providers if p['specialty'].lower() == specialty.lower()]
    
    if carrier_id:
        filtered_providers = [p for p in filtered_providers if carrier_id in p['carrier_networks']]
    
    return filtered_providers[:limit]

def check_provider_in_network(provider_name, carrier_id):
    """
    Check if a provider is in a carrier's network
    
    Args:
        provider_name (str): Name of the provider
        carrier_id (int): Carrier ID
        
    Returns:
        bool: True if in network, False otherwise
    """
    logger.debug(f"Checking if provider {provider_name} is in network for carrier {carrier_id}")
    
    for provider in providers_data:
        if provider['name'].lower() == provider_name.lower():
            return carrier_id in provider['carrier_networks']
    
    return False
