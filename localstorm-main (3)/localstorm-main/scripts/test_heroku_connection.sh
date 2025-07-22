#!/bin/bash

# Simple Heroku PostgreSQL Migration using curl and SQL
# This attempts to use a HTTP-to-PostgreSQL bridge if available

echo "🚀 Attempting Heroku PostgreSQL Migration via Alternative Methods"
echo "================================================================"

# Database URL
DATABASE_URL="postgresql://u8h1en29mru00:p3020c7560854b178b598d2993a2b91173972e98a202f19c9ba981e3bbd8@c7jla3ha5puqsf.cluster-czrs8kj4isg6.us-east-1.rds.amazonaws.com:5432/d5h1tdp6nrlcj8"

# Extract connection details
DB_HOST="c7jla3ha5puqsf.cluster-czrs8kj4isg6.us-east-1.rds.amazonaws.com"
DB_PORT="5432"
DB_NAME="d5h1tdp6nrlcj8"
DB_USER="u8h1en29mru00"
DB_PASS="p3020c7560854b178b598d2993a2b91173972e98a202f19c9ba981e3bbd8"

echo "🔍 Testing database connectivity..."

# Try to ping the database host
if ping -c 1 "$DB_HOST" >/dev/null 2>&1; then
    echo "✅ Host $DB_HOST is reachable"
    
    # Try direct psql connection with timeout
    echo "🔗 Attempting direct PostgreSQL connection..."
    
    timeout 10 psql "$DATABASE_URL" -c "SELECT version();" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully connected to Heroku PostgreSQL!"
        echo "🚀 Running migration..."
        
        # Run the migration
        psql "$DATABASE_URL" -f /workspaces/localstorm/scripts/heroku_migration.sql
        
        if [ $? -eq 0 ]; then
            echo "✅ Migration completed successfully!"
        else
            echo "❌ Migration failed"
        fi
    else
        echo "❌ Could not connect to PostgreSQL database"
        echo "🔧 This is likely due to network restrictions in the dev environment"
    fi
else
    echo "❌ Host $DB_HOST is not reachable from this environment"
    echo "🌐 This is expected in a containerized development environment"
fi

echo ""
echo "📋 MANUAL MIGRATION INSTRUCTIONS:"
echo "=================================="
echo ""
echo "Since automatic migration from this environment failed, please run the migration manually:"
echo ""
echo "1. 💻 On your local machine (with internet access):"
echo "   psql '$DATABASE_URL' -f scripts/heroku_migration.sql"
echo ""
echo "2. 📱 Or using Heroku CLI:"
echo "   heroku pg:psql --app YOUR_APP_NAME"
echo "   Then copy/paste the SQL from scripts/heroku_migration.sql"
echo ""
echo "3. 🌐 Or use a PostgreSQL client like pgAdmin, DBeaver, etc."
echo ""
echo "📁 Migration file location: /workspaces/localstorm/scripts/heroku_migration.sql"
