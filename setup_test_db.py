#!/usr/bin/env python3
"""
Script to set up test database and create admin user
"""
import requests
import time
import json

# Configuration
ODOO_URL = "http://localhost:8069"
DB_NAME = "cbms_test_db"
ADMIN_PASSWORD = "cbms_admin_2024"
ADMIN_EMAIL = "admin@mycbms.com"
COMPANY_NAME = "CBMS TECHNOLOGIES LTD"
COUNTRY = "US"
LANGUAGE = "en_US"

def wait_for_odoo():
    """Wait for Odoo to be ready"""
    print("Waiting for Odoo to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{ODOO_URL}/web/database/selector", timeout=5)
            if response.status_code == 200:
                print("✅ Odoo is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"⏳ Waiting... ({i+1}/30)")
        time.sleep(2)
    
    return False

def create_database():
    """Create the test database"""
    print(f"Creating database: {DB_NAME}")
    
    # Database creation payload
    data = {
        'master_pwd': 'cbms_admin_2024',
        'name': DB_NAME,
        'login': 'admin',
        'password': ADMIN_PASSWORD,
        'phone': '+1-555-0123',
        'lang': LANGUAGE,
        'country_code': COUNTRY,
        'demo': False,  # No demo data
    }
    
    try:
        response = requests.post(
            f"{ODOO_URL}/web/database/create",
            data=data,
            timeout=300  # 5 minutes timeout for database creation
        )
        
        if response.status_code == 200:
            print("✅ Database created successfully!")
            return True
        else:
            print(f"❌ Database creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating database: {e}")
        return False

def test_login():
    """Test login to the created database"""
    print("Testing admin login...")
    
    session = requests.Session()
    
    # Get login page
    try:
        login_response = session.get(f"{ODOO_URL}/web/login?db={DB_NAME}")
        if login_response.status_code != 200:
            print(f"❌ Cannot access login page: {login_response.status_code}")
            return False
        
        # Attempt login
        login_data = {
            'login': 'admin',
            'password': ADMIN_PASSWORD,
            'db': DB_NAME
        }
        
        auth_response = session.post(f"{ODOO_URL}/web/login", data=login_data)
        
        if auth_response.status_code == 200 and 'web/webclient' in auth_response.url:
            print("✅ Admin login successful!")
            return True
        else:
            print(f"❌ Login failed: {auth_response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing login: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Starting Odoo Test Environment Setup")
    print("=" * 50)
    
    # Wait for Odoo to be ready
    if not wait_for_odoo():
        print("❌ Odoo is not responding. Please check the container.")
        return False
    
    # Create database
    if not create_database():
        print("❌ Database creation failed.")
        return False
    
    # Wait a bit for database to be fully initialized
    print("⏳ Waiting for database initialization...")
    time.sleep(10)
    
    # Test login
    if not test_login():
        print("❌ Login test failed.")
        return False
    
    print("\n🎉 Test environment setup complete!")
    print("=" * 50)
    print(f"🌐 URL: {ODOO_URL}")
    print(f"🗄️  Database: {DB_NAME}")
    print(f"👤 Username: admin")
    print(f"🔑 Password: {ADMIN_PASSWORD}")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    main()
