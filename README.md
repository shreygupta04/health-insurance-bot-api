# Insurance AI Voice Bot API

A Flask-based REST API that serves as a testing server for an AI voice bot. This API provides endpoints for handling insurance-related queries, including premium payment assistance, provider lookup, and benefits information.

## API Features

The API is designed to support three core functionality flows:

### 1. Premium Payment Assistance

Provides endpoints for:
- Member authentication using DOB and ZIP code
- Retrieving carrier payment portal information
- Directing members to the appropriate payment portal

**Endpoints:**
- `POST /api/payments/authenticate` - Authenticate a member for payment processing
- `GET /api/payments/portal` - Get payment portal information for a carrier

### 2. In-Network Provider Lookup

Supports finding doctors and facilities that accept a member's insurance plan:
- Search for providers based on location and specialty
- Verify if a specific provider is in-network
- Return provider directory links

**Endpoints:**
- `GET /api/providers` - Search for providers based on filters
- `GET /api/providers/check-network` - Check if a specific provider is in a carrier's network

### 3. Plan Benefits and Coverage Information

Provides access to plan details and coverage information:
- Benefit details including deductibles, copays, and out-of-pocket maximums
- Coverage checks for specific services (dental, vision, mental health)
- Access to Summary of Benefits and Coverage (SBC) documents

**Endpoints:**
- `POST /api/benefits/authenticate` - Authenticate a member to retrieve benefits
- `GET /api/benefits/plan/{plan_id}` - Get detailed benefits for a specific plan
- `GET /api/benefits/coverage` - Check if a specific service is covered by a plan

## Getting Started

### Installation

1. Install dependencies:
```
pip install -r dependencies_list.txt
```

2. Start the application:
```
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### API Documentation

Interactive API documentation is available at `/docs` when the server is running.

### Testing Endpoints

You can test the API using curl:

```bash
# Check health
curl http://localhost:5000/api/health

# Get payment portal info
curl "http://localhost:5000/api/payments/portal?carrier=Ambetter"

# Find providers
curl "http://localhost:5000/api/providers?carrier=Oscar+Health&zip_code=33130"

# Get plan benefits
curl "http://localhost:5000/api/benefits/plan/3"
```

## Security Considerations

- The API includes basic authentication mechanisms using DOB, ZIP code, or Member ID
- It does not process payments directly but provides redirection to carrier payment portals
- All endpoints use HTTPS for secure data transmission
- No sensitive personal health information (PHI) is exposed in responses

---

© 2025 Insurance AI Voice Bot API