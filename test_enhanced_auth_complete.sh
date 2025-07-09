#!/bin/bash

echo "🧪 Testing Enhanced Authentication Endpoints"
echo "============================================="

BASE_URL="https://capecraft-65eeb6ddf78b.herokuapp.com"

echo ""
echo "1. Testing Enhanced Health Endpoint..."
curl -s -w "\nHTTP Status: %{http_code}\n" \
  "$BASE_URL/api/enhanced/health" || echo "❌ Health endpoint failed"

echo ""
echo "2. Testing Enhanced Registration..."
curl -s -w "\nHTTP Status: %{http_code}\n" \
  -X POST "$BASE_URL/api/enhanced/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser4@example.com",
    "password": "SecurePass123!",
    "firstName": "Test",
    "lastName": "User",
    "role": "customer"
  }' \
  --max-time 20 || echo "❌ Registration failed"

echo ""
echo "3. Testing with uppercase role..."
curl -s -w "\nHTTP Status: %{http_code}\n" \
  -X POST "$BASE_URL/api/enhanced/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser5@example.com", 
    "password": "SecurePass123!",
    "firstName": "Test",
    "lastName": "User",
    "role": "CUSTOMER"
  }' \
  --max-time 20 || echo "❌ Registration with uppercase role failed"

echo ""
echo "✅ Testing completed"
