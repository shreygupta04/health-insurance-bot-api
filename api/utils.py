"""
Utility functions for the API
"""
import logging
import re

# Configure logging
logger = logging.getLogger(__name__)

class APIError(Exception):
    """
    Custom exception class for API errors
    """
    def __init__(self, message, status_code=400, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or status_code
        super().__init__(self.message)

def validate_request(**kwargs):
    """
    Validate request parameters
    
    Args:
        **kwargs: Parameters to validate
        
    Raises:
        APIError: If validation fails
    """
    # Validate limit parameter
    if 'limit' in kwargs:
        limit = kwargs['limit']
        if limit is not None:
            if not isinstance(limit, int):
                raise APIError("Limit must be an integer", 400)
            if limit < 1:
                raise APIError("Limit must be a positive integer", 400)
            if limit > 100:
                raise APIError("Limit cannot exceed 100", 400)
    
    # Validate ZIP code parameter
    if 'zip_code' in kwargs and kwargs['zip_code'] is not None:
        zip_code = kwargs['zip_code']
        if not re.match(r'^\d{5}$', zip_code):
            raise APIError("ZIP code must be a 5-digit number", 400)
    
    # Validate date of birth parameter
    if 'dob' in kwargs and kwargs['dob'] is not None:
        dob = kwargs['dob']
        if not re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$', dob):
            raise APIError("Date of birth must be in MM/DD/YYYY format", 400)
    
    # Validate member_id parameter
    if 'member_id' in kwargs and kwargs['member_id'] is not None:
        member_id = kwargs['member_id']
        if not isinstance(member_id, str) or not member_id.startswith('MEM'):
            raise APIError("Member ID must be a string starting with 'MEM'", 400)
    
    # Validate plan_id parameter
    if 'plan_id' in kwargs:
        plan_id = kwargs['plan_id']
        if not isinstance(plan_id, int) or plan_id < 1:
            raise APIError("Plan ID must be a positive integer", 400)
    
    # Validate service parameter
    if 'service' in kwargs and kwargs['service'] is not None:
        service = kwargs['service']
        valid_services = ['dental', 'vision', 'mental_health']
        if service not in valid_services:
            raise APIError(f"Invalid service. Must be one of: {', '.join(valid_services)}", 400)
    
    # Validate specialty parameter
    if 'specialty' in kwargs and kwargs['specialty'] is not None:
        specialty = kwargs['specialty']
        valid_specialties = ['Primary Care', 'Cardiology', 'Pediatrics', 'Orthopedics', 'Dermatology']
        if specialty not in valid_specialties:
            raise APIError(f"Invalid specialty. Must be one of: {', '.join(valid_specialties)}", 400)
    
    # Validate carrier parameter
    if 'carrier' in kwargs and kwargs['carrier'] is not None:
        carrier = kwargs['carrier']
        valid_carriers = ['Ambetter', 'Oscar Health', 'Blue Cross Blue Shield', 'Aetna', 'Cigna']
        if carrier not in valid_carriers:
            raise APIError(f"Invalid carrier. Must be one of: {', '.join(valid_carriers)}", 400)

    logger.debug("Request validation passed")
    return True
