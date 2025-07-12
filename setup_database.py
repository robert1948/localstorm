#!/usr/bin/env python3
import sys
import os
sys.path.append('/workspaces/localstorm/backend')

from app.database import engine, Base
from app.models_enhanced import UserV2, Token, DeveloperEarning, PasswordReset, AuditLog

print("Creating fresh database with Phase 2 fields...")

# Drop and create all tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Verify the Phase 2 fields
from sqlalchemy import inspect
inspector = inspect(engine)

print("\nVerifying tables...")
tables = inspector.get_table_names()
print(f"Created tables: {tables}")

if 'users_v2' in tables:
    columns = inspector.get_columns('users_v2')
    print(f"\nusers_v2 has {len(columns)} columns:")
    
    # List all columns
    for i, col in enumerate(columns, 1):
        print(f"  {i:2d}. {col['name']}: {col['type']}")
    
    # Check specific Phase 2 fields
    phase2_fields = [
        'profile_completed', 'phase2_completed', 'company_name', 'industry', 
        'company_size', 'business_type', 'use_case', 'budget', 'goals', 
        'preferred_integrations', 'timeline', 'experience_level', 
        'primary_languages', 'specializations', 'github_profile', 
        'portfolio_url', 'social_links', 'previous_projects', 'availability', 
        'hourly_rate', 'earnings_target', 'revenue_share'
    ]
    
    found_fields = [col['name'] for col in columns if col['name'] in phase2_fields]
    print(f"\nPhase 2 fields ({len(found_fields)}/{len(phase2_fields)}):")
    for field in found_fields:
        print(f"  ✅ {field}")
    
    missing_fields = [field for field in phase2_fields if field not in found_fields]
    if missing_fields:
        print(f"\nMissing fields:")
        for field in missing_fields:
            print(f"  ❌ {field}")
    
    if len(found_fields) == len(phase2_fields):
        print("\n🎉 SUCCESS: All Phase 2 fields created!")
    else:
        print(f"\n❌ PARTIAL: {len(found_fields)}/{len(phase2_fields)} Phase 2 fields created")

print("\n✅ Database setup complete!")
