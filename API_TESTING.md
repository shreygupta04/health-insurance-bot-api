# API Testing Guide

This document provides examples for testing the Insurance AI Voice Bot API endpoints.

## Base URL

The API is hosted at: `http://localhost:5000/api`

## Health Check

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "success",
  "message": "API is running"
}
```

## 1. Premium Payment Assistance

### Authenticate for Payment

```bash
curl -X POST http://localhost:5000/api/payments/authenticate \
  -H "Content-Type: application/json" \
  -d '{"dob": "01/15/1985", "zip_code": "78745"}'
```

Alternative with member ID:
```bash
curl -X POST http://localhost:5000/api/payments/authenticate \
  -H "Content-Type: application/json" \
  -d '{"member_id": "MEM12345"}'
```

### Get Payment Portal Information

```bash
curl "http://localhost:5000/api/payments/portal?carrier=Ambetter"
```

Expected response:
```json
{
  "success": true,
  "data": {
    "name": "Ambetter",
    "payment_portal": "https://ambetter.paymentportal.com",
    "payment_phone": "1-800-123-4567",
    "spanish_support": true,
    "customer_service": "1-888-123-4567"
  }
}
```

## 2. In-Network Provider Lookup

### Search for Providers

```bash
# Search by ZIP code
curl "http://localhost:5000/api/providers?zip_code=78745"

# Search by specialty
curl "http://localhost:5000/api/providers?specialty=Primary+Care"

# Search by carrier
curl "http://localhost:5000/api/providers?carrier=Oscar+Health"

# Combined search
curl "http://localhost:5000/api/providers?carrier=Oscar+Health&zip_code=33130&specialty=Cardiology"
```

### Check if Provider is In-Network

```bash
curl "http://localhost:5000/api/providers/check-network?provider_name=Dr.+Sarah+Johnson&carrier=Ambetter"
```

Expected response:
```json
{
  "success": true,
  "data": {
    "provider_name": "Dr. Sarah Johnson",
    "carrier": "Ambetter",
    "in_network": true,
    "provider_directory": "https://ambetter.providerdirectory.com"
  }
}
```

## 3. Plan Benefits and Coverage Information

### Authenticate for Benefits

```bash
curl -X POST http://localhost:5000/api/benefits/authenticate \
  -H "Content-Type: application/json" \
  -d '{"dob": "01/15/1985", "zip_code": "78745"}'
```

### Get Plan Benefits

```bash
curl "http://localhost:5000/api/benefits/plan/1"
```

Expected response:
```json
{
  "success": true,
  "data": {
    "plan_name": "Ambetter SecureCare Bronze 2025",
    "carrier": "Ambetter",
    "type": "Bronze",
    "deductible": 8000,
    "out_of_pocket_max": 9000,
    "copays": {
      "primary_care": 40,
      "specialist": 80,
      "emergency": 500,
      "urgent_care": 75,
      "generic_drugs": 25
    },
    "coverage": {
      "dental": false,
      "vision": false,
      "mental_health": true
    },
    "sbc_url": "https://ambetter.com/sbc/bronze2025.pdf",
    "customer_service": "1-888-123-4567"
  }
}
```

### Check Service Coverage

```bash
# Check if dental is covered
curl "http://localhost:5000/api/benefits/coverage?plan_id=1&service=dental"

# Check if vision is covered
curl "http://localhost:5000/api/benefits/coverage?plan_id=2&service=vision"

# Check if mental health is covered
curl "http://localhost:5000/api/benefits/coverage?plan_id=3&service=mental_health"
```

Expected response:
```json
{
  "success": true,
  "data": {
    "plan_name": "Ambetter SecureCare Bronze 2025",
    "service": "dental",
    "is_covered": false
  }
}
```

## Error Handling

### Authentication Failure

```bash
curl -X POST http://localhost:5000/api/payments/authenticate \
  -H "Content-Type: application/json" \
  -d '{"dob": "01/01/1990", "zip_code": "12345"}'
```

Expected response:
```json
{
  "success": false,
  "error": 401,
  "message": "Authentication failed. Please check your information."
}
```

### Resource Not Found

```bash
curl "http://localhost:5000/api/benefits/plan/999"
```

Expected response:
```json
{
  "success": false,
  "error": 404,
  "message": "Plan with ID 999 not found"
}
```

### Bad Request

```bash
curl "http://localhost:5000/api/benefits/coverage?plan_id=1&service=invalid"
```

Expected response:
```json
{
  "success": false,
  "error": 400,
  "message": "Invalid service. Must be one of: dental, vision, mental_health"
}
```