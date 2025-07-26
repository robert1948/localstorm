#!/bin/bash

# This script is intended to run tests for the localstorm AI project.

# Navigate to the backend directory and run backend tests
echo "Running backend tests..."
cd backend
npm test

# Navigate to the frontend directory and run frontend tests
echo "Running frontend tests..."
cd ../frontend
npm test

# Navigate to the mobile directory and run mobile tests
echo "Running mobile tests..."
cd ../mobile
npm test

echo "All tests completed."