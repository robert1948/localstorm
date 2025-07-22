# 🔗 **LocalStorm + Heroku Database Configuration Guide**

## 🎯 **Objective**: Run LocalStorm locally connected to Heroku cape-craft production database

### **Step 1: Get Heroku Database URL**

```bash
# Login to Heroku (will open browser for authentication)
heroku login

# Get the database URL for cape-craft app
heroku config:get DATABASE_URL -a cape-craft

# Alternative: View all config vars
heroku config -a cape-craft
```

**Expected format:**
```
postgresql://username:password@host:port/database_name
```

### **Step 2: Update Local Environment**

Copy the DATABASE_URL from Heroku and update your `.env` file:

```bash
# Replace the SQLite URL with your Heroku PostgreSQL URL
DATABASE_URL=postgresql://your_heroku_db_url_here
```

### **Step 3: Install PostgreSQL Dependencies**

```bash
# Install psycopg2 for PostgreSQL connectivity (already installed)
pip install psycopg2-binary
```

### **Step 4: Update Database Configuration**

The application will automatically:
- ✅ Connect to PostgreSQL instead of SQLite
- ✅ Use existing production data and schema
- ✅ Run with live data (be careful with modifications!)

### **Step 5: Start LocalStorm**

```bash
# Stop current local instance
pkill -f "uvicorn|vite"

# Start with new database configuration
./scripts/start_localstorm.sh
```

### **🔥 Important Notes:**

1. **⚠️ Production Data**: You'll be working with LIVE production data
2. **🔐 Security**: Never commit the production DATABASE_URL to git
3. **🧪 Testing**: Consider using a staging database for development
4. **📊 Performance**: Network latency will be higher than local SQLite

### **🛡️ Safety Recommendations:**

1. **Use read-only operations** for development when possible
2. **Create a development branch** in Heroku for safer testing
3. **Backup before major changes** if modifying data
4. **Test thoroughly** before deploying changes

### **🚀 Expected Result:**

- ✅ **Frontend**: http://localhost:3001 (React app)
- ✅ **Backend**: http://localhost:8000 (FastAPI connected to Heroku DB)
- ✅ **Database**: Production PostgreSQL on Heroku
- ✅ **Data**: Live production users, registrations, etc.
