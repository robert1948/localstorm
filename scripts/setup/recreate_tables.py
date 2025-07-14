#!/usr/bin/env python3
import sys
sys.path.append('/workspaces/localstorm/backend')

from app.database import engine, Base
from app.models_enhanced import UserV2

# Force drop and recreate
print("Dropping tables...")
Base.metadata.drop_all(bind=engine)

print("Creating tables...")  
Base.metadata.create_all(bind=engine)

# Verify
from sqlalchemy import inspect
inspector = inspect(engine)
columns = inspector.get_columns('users_v2')
print(f"Created users_v2 with {len(columns)} columns")

phase2_fields = ['profile_completed', 'phase2_completed', 'company_name', 'industry']
found = [col['name'] for col in columns if col['name'] in phase2_fields]
print(f"Phase 2 fields found: {found}")

if len(found) == len(phase2_fields):
    print("✅ SUCCESS: All Phase 2 fields created!")
else:
    print("❌ FAILED: Phase 2 fields missing")
    print("Expected:", phase2_fields)
    print("Found:", found)
