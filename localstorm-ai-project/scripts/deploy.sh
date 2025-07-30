#!/bin/bash

# This script is used to deploy the localstorm AI project.

# Set environment variables
export NODE_ENV=production

# Navigate to the backend directory and install dependencies
cd backend
npm install --production

# Build the backend application
npm run build

# Navigate to the frontend directory and install dependencies
cd ../frontend
npm install --production

# Build the frontend application
npm run build

# Navigate to the mobile directory and install dependencies
cd ../mobile
npm install --production

# Build the mobile application
npm run build

# Start the backend server
cd ../backend
npm start &

# Start the frontend server
cd ../frontend
npm start &

# Start the mobile application (if applicable)
cd ../mobile
npm start &

echo "Deployment completed successfully."