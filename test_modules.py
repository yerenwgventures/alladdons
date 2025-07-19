#!/usr/bin/env python3
"""
Comprehensive module testing script for CBMS Odoo modules
Tests each module installation and logs any errors
"""
import os
import requests
import json
import time
import subprocess
from datetime import datetime

class OdooModuleTester:
    def __init__(self):
        self.base_url = "http://localhost:8069"
        self.db_name = "cbms_test_db"
        self.username = "admin"
        self.password = "cbms_admin_2024"
        self.session = requests.Session()
        self.test_results = []
        
    def get_odoo_logs(self, lines=20):
        """Get recent Odoo logs"""
        try:
            result = subprocess.run(
                ["docker", "logs", "odoo_test_instance", "--tail", str(lines)],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Error getting logs: {e}"
    
    def check_for_errors_in_logs(self, module_name):
        """Check for errors related to specific module in logs"""
        logs = self.get_odoo_logs(50)
        error_keywords = ["ERROR", "CRITICAL", "Exception", "Traceback", "Failed"]
        
        errors = []
        for line in logs.split('\n'):
            if any(keyword in line for keyword in error_keywords):
                if module_name.lower() in line.lower() or any(keyword in line for keyword in error_keywords):
                    errors.append(line.strip())
        
        return errors
    
    def login(self):
        """Login to Odoo"""
        print("🔐 Logging into Odoo...")
        
        # Get login page first
        login_page = self.session.get(f"{self.base_url}/web/login?db={self.db_name}")
        if login_page.status_code != 200:
            print(f"❌ Cannot access login page: {login_page.status_code}")
            return False
        
        # Extract CSRF token if present
        csrf_token = None
        if 'csrf_token' in login_page.text:
            import re
            token_match = re.search(r'csrf_token["\']:\s*["\']([^"\']+)["\']', login_page.text)
            if token_match:
                csrf_token = token_match.group(1)
        
        # Login data
        login_data = {
            'login': self.username,
            'password': self.password,
            'db': self.db_name
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
        
        # Attempt login
        response = self.session.post(f"{self.base_url}/web/login", data=login_data)
        
        if response.status_code == 200 and 'web' in response.url:
            print("✅ Login successful!")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
    
    def get_module_list(self):
        """Get list of available modules"""
        print("📋 Getting module list...")
        
        # Get modules from filesystem
        modules = []
        for item in os.listdir('.'):
            if os.path.isdir(item) and os.path.exists(os.path.join(item, '__manifest__.py')):
                modules.append(item)
        
        # Filter out system modules and testing files
        excluded = ['config', 'logs', '__pycache__', '.git', '.github']
        modules = [m for m in modules if m not in excluded and not m.startswith('.')]
        
        print(f"✅ Found {len(modules)} modules to test")
        return sorted(modules)
    
    def install_module(self, module_name):
        """Install a specific module"""
        print(f"\n🔧 Installing module: {module_name}")
        
        # Check logs before installation
        logs_before = self.get_odoo_logs(10)
        
        try:
            # Use Odoo CLI to install module
            install_cmd = [
                "docker", "exec", "odoo_test_instance",
                "odoo", "-d", self.db_name,
                "-i", module_name,
                "--stop-after-init"
            ]
            
            result = subprocess.run(
                install_cmd, 
                capture_output=True, 
                text=True, 
                timeout=120
            )
            
            # Check logs after installation
            time.sleep(2)
            logs_after = self.get_odoo_logs(20)
            errors = self.check_for_errors_in_logs(module_name)
            
            success = result.returncode == 0 and len(errors) == 0
            
            test_result = {
                'module': module_name,
                'success': success,
                'return_code': result.returncode,
                'stdout': result.stdout[-500:] if result.stdout else "",
                'stderr': result.stderr[-500:] if result.stderr else "",
                'errors_found': errors,
                'timestamp': datetime.now().isoformat()
            }
            
            self.test_results.append(test_result)
            
            if success:
                print(f"✅ {module_name} installed successfully")
            else:
                print(f"❌ {module_name} installation failed")
                if errors:
                    print("   Errors found:")
                    for error in errors[:3]:  # Show first 3 errors
                        print(f"   - {error}")
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"⏰ {module_name} installation timed out")
            return False
        except Exception as e:
            print(f"❌ Error installing {module_name}: {e}")
            return False
    
    def restart_odoo(self):
        """Restart Odoo container"""
        print("🔄 Restarting Odoo...")
        try:
            subprocess.run(["docker-compose", "restart", "odoo"], 
                         cwd="/mnt/persist/workspace", timeout=60)
            time.sleep(10)  # Wait for restart
            print("✅ Odoo restarted")
            return True
        except Exception as e:
            print(f"❌ Error restarting Odoo: {e}")
            return False
    
    def generate_report(self):
        """Generate test report"""
        print("\n📊 Generating test report...")
        
        total_modules = len(self.test_results)
        successful = len([r for r in self.test_results if r['success']])
        failed = total_modules - successful
        
        report = f"""
# CBMS MODULE TESTING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## SUMMARY
- Total modules tested: {total_modules}
- Successful installations: {successful}
- Failed installations: {failed}
- Success rate: {(successful/total_modules*100):.1f}%

## FAILED MODULES
"""
        
        for result in self.test_results:
            if not result['success']:
                report += f"\n### {result['module']}\n"
                report += f"- Return code: {result['return_code']}\n"
                if result['errors_found']:
                    report += "- Errors:\n"
                    for error in result['errors_found'][:2]:
                        report += f"  - {error}\n"
        
        # Save report
        with open('module_test_report.md', 'w') as f:
            f.write(report)
        
        print("✅ Report saved to module_test_report.md")
        return report
    
    def run_tests(self, max_modules=10):
        """Run tests on modules"""
        print("🚀 Starting module testing...")
        print("=" * 60)
        
        modules = self.get_module_list()
        
        # Test first batch of modules
        test_modules = modules[:max_modules]
        
        print(f"📝 Testing first {len(test_modules)} modules:")
        for i, module in enumerate(test_modules, 1):
            print(f"   {i}. {module}")
        
        print("=" * 60)
        
        for i, module in enumerate(test_modules, 1):
            print(f"\n[{i}/{len(test_modules)}] Testing: {module}")
            
            success = self.install_module(module)
            
            if not success:
                print(f"⚠️  Module {module} failed - continuing with next module")
            
            # Small delay between installations
            time.sleep(1)
        
        # Generate final report
        report = self.generate_report()
        print("\n" + "=" * 60)
        print("🎉 Testing completed!")
        print("=" * 60)
        
        return self.test_results

def main():
    tester = OdooModuleTester()
    
    print("🧪 CBMS MODULE TESTING FRAMEWORK")
    print("=" * 60)
    
    # Run tests on first 10 modules
    results = tester.run_tests(max_modules=10)
    
    return results

if __name__ == "__main__":
    main()
