#!/bin/bash

# This script sets up the local environment for the LocalStorm AI project.

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install Node.js and npm
echo "Installing Node.js and npm..."
sudo apt-get install -y nodejs npm

# Install TypeScript globally
echo "Installing TypeScript globally..."
sudo npm install -g typescript

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y docker.io

# Install Docker Compose
echo "Installing Docker Compose..."
sudo apt-get install -y docker-compose

# Navigate to the backend directory and install dependencies
echo "Installing backend dependencies..."
cd backend
npm install

# Navigate to the frontend directory and install dependencies
echo "Installing frontend dependencies..."
cd ../frontend
npm install

# Navigate to the mobile directory and install dependencies
echo "Installing mobile dependencies..."
cd ../mobile
npm install

# Return to the root directory
cd ..

# Setup complete
echo "Setup complete! You can now run the project."