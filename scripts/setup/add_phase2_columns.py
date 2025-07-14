#!/usr/bin/env python3
"""
Add Phase 2 Columns Migration
============================
Adds Phase 2 profile columns to the existing users_v2 table.
"""

import sys
import os
sys.path.append('/workspaces/localstorm/backend')

from app.database import engine
from sqlalchemy import text

def add_phase2_columns():
    """Add Phase 2 columns to users_v2 table"""
    
    phase2_columns = [
        ('profile_completed', 'BOOLEAN DEFAULT FALSE NOT NULL'),
        ('phase2_completed', 'BOOLEAN DEFAULT FALSE NOT NULL'),
        ('company_name', 'VARCHAR(255)'),
        ('industry', 'VARCHAR(100)'),
        ('company_size', 'VARCHAR(50)'),
        ('business_type', 'VARCHAR(50)'),
        ('use_case', 'VARCHAR(100)'),
        ('budget', 'VARCHAR(50)'),
        ('goals', 'JSONB'),
        ('preferred_integrations', 'JSONB'),
        ('timeline', 'VARCHAR(50)'),
        ('experience_level', 'VARCHAR(50)'),
        ('primary_languages', 'JSONB'),
        ('specializations', 'JSONB'),
        ('github_profile', 'VARCHAR(255)'),
        ('portfolio_url', 'VARCHAR(255)'),
        ('social_links', 'JSONB'),
        ('previous_projects', 'TEXT'),
        ('availability', 'VARCHAR(50)'),
        ('hourly_rate', 'VARCHAR(50)'),
        ('earnings_target', 'VARCHAR(50)'),
        ('revenue_share', 'NUMERIC(5,4) DEFAULT 0.3000')
    ]
    
    print("Adding Phase 2 columns to users_v2 table...")
    
    with engine.connect() as conn:
        # Check existing columns
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'users_v2' AND table_schema = 'public'
        """))
        existing_columns = [row[0] for row in result]
        print(f"Existing columns: {len(existing_columns)}")
        
        # Add missing columns
        added_count = 0
        for column_name, column_def in phase2_columns:
            if column_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE users_v2 ADD COLUMN {column_name} {column_def}"
                    conn.execute(text(sql))
                    print(f"✅ Added column: {column_name}")
                    added_count += 1
                except Exception as e:
                    print(f"❌ Failed to add {column_name}: {e}")
            else:
                print(f"⚠️  Column {column_name} already exists")
        
        conn.commit()
        
        # Verify
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'users_v2' AND table_schema = 'public'
        """))
        final_columns = [row[0] for row in result]
        print(f"\nFinal column count: {len(final_columns)}")
        print(f"Added {added_count} new columns")
        
        # Check for Phase 2 columns
        phase2_found = [col for col in final_columns if col in [name for name, _ in phase2_columns]]
        print(f"Phase 2 columns present: {len(phase2_found)}/{len(phase2_columns)}")
        
        if len(phase2_found) == len(phase2_columns):
            print("🎉 All Phase 2 columns added successfully!")
            return True
        else:
            print("❌ Some Phase 2 columns are missing")
            return False

if __name__ == "__main__":
    try:
        success = add_phase2_columns()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)
