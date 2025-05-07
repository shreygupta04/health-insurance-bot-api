from flask import Blueprint, jsonify, request
from api.models import (
    authenticate_member, get_carrier, get_carrier_by_name, get_plan,
    get_member_plan, get_providers, check_provider_in_network
)
from api.utils import validate_request, APIError
import logging

# Configure logging
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint to check if the API is running
    ---
    responses:
      200:
        description: API is running
    """
    return jsonify({
        'status': 'success',
        'message': 'API is running'
    })

# 1. Premium Payment Assistance API Endpoints
@api_bp.route('/payments/authenticate', methods=['POST'])
def authenticate_for_payment():
    """
    Authenticate a member for payment processing
    ---
    parameters:
      - name: dob
        in: body
        type: string
        description: Date of birth in MM/DD/YYYY format
      - name: zip_code
        in: body
        type: string
        description: ZIP code
      - name: member_id
        in: body
        type: string
        description: Member ID (alternative to DOB + ZIP)
    responses:
      200:
        description: Authentication successful
      401:
        description: Authentication failed
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        dob = data.get('dob')
        zip_code = data.get('zip_code')
        member_id = data.get('member_id')
        
        # Authenticate member
        if member_id:
            member = authenticate_member(member_id=member_id)
        elif dob and zip_code:
            member = authenticate_member(dob=dob, zip_code=zip_code)
        else:
            raise APIError("Authentication requires either Member ID or DOB + ZIP Code", 400)
        
        if not member:
            return jsonify({
                'success': False,
                'error': 401,
                'message': 'Authentication failed. Please check your information.'
            }), 401
        
        # Get carrier information
        carrier_name = member['carrier']
        carrier = get_carrier_by_name(carrier_name)
        
        # Get member's plan
        plan = get_plan(member['plan_id'])
        
        return jsonify({
            'success': True,
            'data': {
                'member': {
                    'first_name': member['first_name'],
                    'last_name': member['last_name'],
                    'member_id': member['member_id'],
                    'phone_last_four': member['phone'][-4:]
                },
                'carrier': {
                    'name': carrier['name'],
                    'payment_portal': carrier['payment_portal'],
                    'payment_phone': carrier['payment_phone'],
                    'spanish_support': carrier['spanish_support']
                },
                'plan': {
                    'name': plan['name'],
                    'type': plan['type']
                }
            }
        })
    except APIError as e:
        logger.error(f"API error in authenticate_for_payment endpoint: {e}")
        return jsonify({
            'success': False,
            'error': e.error_code,
            'message': str(e)
        }), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in authenticate_for_payment endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

@api_bp.route('/payments/portal', methods=['GET'])
def payment_portal_info():
    """
    Get payment portal information for a carrier
    ---
    parameters:
      - name: carrier
        in: query
        type: string
        required: true
        description: Name of the insurance carrier
    responses:
      200:
        description: Payment portal information
      404:
        description: Carrier not found
    """
    try:
        carrier_name = request.args.get('carrier')
        if not carrier_name:
            raise APIError("Carrier name is required", 400)
        
        carrier = get_carrier_by_name(carrier_name)
        if not carrier:
            return jsonify({
                'success': False,
                'error': 404,
                'message': f'Carrier "{carrier_name}" not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'name': carrier['name'],
                'payment_portal': carrier['payment_portal'],
                'payment_phone': carrier['payment_phone'],
                'spanish_support': carrier['spanish_support'],
                'customer_service': carrier['customer_service']
            }
        })
    except APIError as e:
        logger.error(f"API error in payment_portal_info endpoint: {e}")
        return jsonify({
            'success': False,
            'error': e.error_code,
            'message': str(e)
        }), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in payment_portal_info endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

# 2. In-Network Provider Lookup API Endpoints
@api_bp.route('/providers', methods=['GET'])
def provider_search():
    """
    Search for providers based on location, specialty, and carrier
    ---
    parameters:
      - name: zip_code
        in: query
        type: string
        description: ZIP code for location-based search
      - name: specialty
        in: query
        type: string
        description: Provider specialty (e.g., Primary Care, Cardiology)
      - name: carrier
        in: query
        type: string
        description: Insurance carrier name
      - name: limit
        in: query
        type: integer
        description: Maximum number of providers to return
    responses:
      200:
        description: List of providers
      404:
        description: No providers found
    """
    try:
        # Get query parameters
        zip_code = request.args.get('zip_code')
        specialty = request.args.get('specialty')
        carrier_name = request.args.get('carrier')
        limit = request.args.get('limit', default=10, type=int)
        
        # Validate parameters
        validate_request(limit=limit)
        
        # Get carrier ID if carrier name provided
        carrier_id = None
        if carrier_name:
            carrier = get_carrier_by_name(carrier_name)
            if carrier:
                carrier_id = carrier['id']
            else:
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': f'Carrier "{carrier_name}" not found'
                }), 404
        
        # Get providers
        providers = get_providers(zip_code=zip_code, specialty=specialty, carrier_id=carrier_id, limit=limit)
        
        if not providers:
            return jsonify({
                'success': False,
                'error': 404,
                'message': 'No providers found matching your criteria'
            }), 404
        
        return jsonify({
            'success': True,
            'count': len(providers),
            'data': providers
        })
    except APIError as e:
        logger.error(f"API error in provider_search endpoint: {e}")
        return jsonify({
            'success': False,
            'error': e.error_code,
            'message': str(e)
        }), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in provider_search endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

@api_bp.route('/providers/check-network', methods=['GET'])
def check_provider_network():
    """
    Check if a specific provider is in a carrier's network
    ---
    parameters:
      - name: provider_name
        in: query
        type: string
        required: true
        description: Name of the provider
      - name: carrier
        in: query
        type: string
        required: true
        description: Name of the insurance carrier
    responses:
      200:
        description: Network status check result
      400:
        description: Missing required parameters
      404:
        description: Carrier not found
    """
    try:
        provider_name = request.args.get('provider_name')
        carrier_name = request.args.get('carrier')
        
        if not provider_name or not carrier_name:
            raise APIError("Both provider_name and carrier are required", 400)
        
        carrier = get_carrier_by_name(carrier_name)
        if not carrier:
            return jsonify({
                'success': False,
                'error': 404,
                'message': f'Carrier "{carrier_name}" not found'
            }), 404
        
        in_network = check_provider_in_network(provider_name, carrier['id'])
        
        return jsonify({
            'success': True,
            'data': {
                'provider_name': provider_name,
                'carrier': carrier_name,
                'in_network': in_network,
                'provider_directory': carrier['provider_directory']
            }
        })
    except APIError as e:
        logger.error(f"API error in check_provider_network endpoint: {e}")
        return jsonify({
            'success': False,
            'error': e.error_code,
            'message': str(e)
        }), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in check_provider_network endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

# 3. Plan Benefits and Coverage Information API Endpoints
@api_bp.route('/benefits/authenticate', methods=['POST'])
def authenticate_for_benefits():
    """
    Authenticate a member to retrieve plan benefits
    ---
    parameters:
      - name: dob
        in: body
        type: string
        description: Date of birth in MM/DD/YYYY format
      - name: zip_code
        in: body
        type: string
        description: ZIP code
      - name: member_id
        in: body
        type: string
        description: Member ID (alternative to DOB + ZIP)
    responses:
      200:
        description: Authentication successful
      401:
        description: Authentication failed
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        dob = data.get('dob')
        zip_code = data.get('zip_code')
        member_id = data.get('member_id')
        
        # Authenticate member
        if member_id:
            member = authenticate_member(member_id=member_id)
        elif dob and zip_code:
            member = authenticate_member(dob=dob, zip_code=zip_code)
        else:
            raise APIError("Authentication requires either Member ID or DOB + ZIP Code", 400)
        
        if not member:
            return jsonify({
                'success': False,
                'error': 401,
                'message': 'Authentication failed. Please check your information.'
            }), 401
        
        return jsonify({
            'success': True,
            'data': {
                'member_id': member['id'],
                'first_name': member['first_name'],
                'last_name': member['last_name'],
                'plan_id': member['plan_id'],
                'carrier': member['carrier']
            }
        })
    except APIError as e:
        logger.error(f"API error in authenticate_for_benefits endpoint: {e}")
        return jsonify({
            'success': False,
            'error': e.error_code,
            'message': str(e)
        }), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in authenticate_for_benefits endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

@api_bp.route('/benefits/plan/<int:plan_id>', methods=['GET'])
def plan_benefits(plan_id):
    """
    Get detailed benefits information for a specific plan
    ---
    parameters:
      - name: plan_id
        in: path
        type: integer
        required: true
        description: ID of the plan
    responses:
      200:
        description: Plan benefits information
      404:
        description: Plan not found
    """
    try:
        plan = get_plan(plan_id)
        
        if not plan:
            return jsonify({
                'success': False,
                'error': 404,
                'message': f'Plan with ID {plan_id} not found'
            }), 404
        
        # Get carrier information
        carrier = get_carrier(plan['carrier_id'])
        
        return jsonify({
            'success': True,
            'data': {
                'plan_name': plan['name'],
                'carrier': carrier['name'],
                'type': plan['type'],
                'deductible': plan['deductible'],
                'out_of_pocket_max': plan['out_of_pocket_max'],
                'copays': {
                    'primary_care': plan['primary_care_copay'],
                    'specialist': plan['specialist_copay'],
                    'emergency': plan['emergency_copay'],
                    'urgent_care': plan['urgent_care_copay'],
                    'generic_drugs': plan['generic_drug_copay']
                },
                'coverage': {
                    'dental': plan['covers_dental'],
                    'vision': plan['covers_vision'],
                    'mental_health': plan['covers_mental_health']
                },
                'sbc_url': plan['sbc_url'],
                'customer_service': carrier['customer_service']
            }
        })
    except APIError as e:
        logger.error(f"API error in plan_benefits endpoint: {e}")
        return jsonify({
            'success': False,
            'error': e.error_code,
            'message': str(e)
        }), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in plan_benefits endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

@api_bp.route('/benefits/coverage', methods=['GET'])
def coverage_check():
    """
    Check if a specific service is covered by a plan
    ---
    parameters:
      - name: plan_id
        in: query
        type: integer
        required: true
        description: ID of the plan
      - name: service
        in: query
        type: string
        required: true
        description: Service to check (dental, vision, mental_health)
    responses:
      200:
        description: Coverage check result
      400:
        description: Invalid service type
      404:
        description: Plan not found
    """
    try:
        plan_id = request.args.get('plan_id', type=int)
        service = request.args.get('service')
        
        if not plan_id or not service:
            raise APIError("Both plan_id and service are required", 400)
        
        plan = get_plan(plan_id)
        if not plan:
            return jsonify({
                'success': False,
                'error': 404,
                'message': f'Plan with ID {plan_id} not found'
            }), 404
        
        valid_services = ['dental', 'vision', 'mental_health']
        if service not in valid_services:
            raise APIError(f"Invalid service. Must be one of: {', '.join(valid_services)}", 400)
        
        is_covered = plan[f'covers_{service}']
        
        return jsonify({
            'success': True,
            'data': {
                'plan_name': plan['name'],
                'service': service,
                'is_covered': is_covered
            }
        })
    except APIError as e:
        logger.error(f"API error in coverage_check endpoint: {e}")
        return jsonify({
            'success': False,
            'error': e.error_code,
            'message': str(e)
        }), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in coverage_check endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500
