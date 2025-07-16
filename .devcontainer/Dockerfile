# Use official Python 3.11 Dev Container base
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install Node.js 20 and clean up to reduce image size
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Optional: Upgrade pip and install pipenv (if needed)
# RUN pip install --upgrade pip pipenv

# Set working directory
WORKDIR /workspace
