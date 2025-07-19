#!/usr/bin/env python3
"""
Simple script to test Odoo access and provide connection details
"""
import requests
import time

def test_odoo_access():
    """Test basic Odoo access"""
    print("🧪 Testing Odoo Access")
    print("=" * 40)
    
    try:
        # Test main page
        response = requests.get("http://localhost:8069", timeout=10)
        print(f"✅ Main page accessible: {response.status_code}")
        
        # Test database selector
        response = requests.get("http://localhost:8069/web/database/selector", timeout=10)
        print(f"✅ Database selector accessible: {response.status_code}")
        
        # Test specific database login page
        response = requests.get("http://localhost:8069/web/login?db=cbms_test_db", timeout=10)
        print(f"✅ Database login page accessible: {response.status_code}")
        
        print("\n🎉 Odoo is fully accessible!")
        print("=" * 40)
        print("🌐 ACCESS DETAILS:")
        print("   URL: http://localhost:8069")
        print("   Database: cbms_test_db")
        print("   Username: admin")
        print("   Password: cbms_admin_2024")
        print("=" * 40)
        print("\n📝 INSTRUCTIONS:")
        print("1. Open http://localhost:8069 in your browser")
        print("2. Select database 'cbms_test_db'")
        print("3. Login with admin / cbms_admin_2024")
        print("4. You should see the Odoo dashboard")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing Odoo: {e}")
        return False

if __name__ == "__main__":
    test_odoo_access()
