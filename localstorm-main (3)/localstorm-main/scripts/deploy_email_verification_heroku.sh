#!/bin/bash

# Heroku PostgreSQL Migration Script for Email Verification
# This script updates the Heroku PostgreSQL database with email verification functionality

echo "🚀 Starting Heroku PostgreSQL migration for email verification..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo -e "${RED}❌ Heroku CLI is not installed. Please install it first.${NC}"
    echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Set app name (you may need to change this)
APP_NAME="cape-control-app"  # Replace with your actual Heroku app name

echo -e "${BLUE}📱 Heroku App: ${APP_NAME}${NC}"

# Check if user is logged into Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo -e "${RED}❌ Please login to Heroku first: heroku login${NC}"
    exit 1
fi

# Get database info
echo -e "${YELLOW}📊 Getting database information...${NC}"
heroku pg:info --app $APP_NAME

# Run the migration
echo -e "${YELLOW}🔧 Running email verification migration...${NC}"

# Method 1: Run the migration script on Heroku
heroku run python migrate_email_verification.py --app $APP_NAME

# Check if migration was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migration completed successfully!${NC}"
    
    # Verify the table was created
    echo -e "${YELLOW}🔍 Verifying table creation...${NC}"
    heroku pg:psql --app $APP_NAME --command "\\d verification_codes"
    
    echo -e "${GREEN}🎉 Email verification is now ready on Heroku!${NC}"
    
    # Show table structure
    echo -e "${YELLOW}📋 Table structure:${NC}"
    heroku pg:psql --app $APP_NAME --command "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'verification_codes' ORDER BY ordinal_position;"
    
else
    echo -e "${RED}❌ Migration failed. Please check the logs.${NC}"
    echo -e "${YELLOW}📋 Getting recent logs:${NC}"
    heroku logs --tail --app $APP_NAME
    exit 1
fi

echo -e "${BLUE}📚 Next steps:${NC}"
echo "1. Deploy your updated app code to Heroku"
echo "2. Test the email verification functionality"
echo "3. Monitor logs for any issues"

echo -e "${GREEN}✨ Migration script completed!${NC}"
