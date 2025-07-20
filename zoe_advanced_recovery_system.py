#!/usr/bin/env python3
"""
ZOE 100x ENGINEER - ADVANCED RECOVERY SYSTEM
Targeted fixes for specific failure patterns to maximize module installation success
"""
import subprocess
import json
import time
import os
from pathlib import Path

class ZoeAdvancedRecovery:
    def __init__(self):
        self.failed_modules = self.load_failed_modules()
        self.success_count = 0
        self.recovery_strategies = {
            'registry_failure': self.fix_registry_failure,
            'xml_structure': self.fix_xml_structure,
            'database_conflict': self.fix_database_conflict,
            'dependency_missing': self.fix_dependency_missing
        }
    
    def load_failed_modules(self):
        """Load failed modules from previous results"""
        try:
            with open('zoe_final_100_percent_results.json', 'r') as f:
                data = json.load(f)
                return data.get('failed_modules', [])
        except:
            return []
    
    def categorize_failure(self, error_msg):
        """Categorize failure type for targeted recovery"""
        error_lower = error_msg.lower()
        
        if 'failed to load registry' in error_lower:
            return 'registry_failure'
        elif 'element odoo has extra content' in error_lower:
            return 'xml_structure'
        elif 'on conflict do update' in error_lower:
            return 'database_conflict'
        elif 'module' in error_lower and ('not found' in error_lower or 'missing' in error_lower):
            return 'dependency_missing'
        else:
            return 'unknown'
    
    def fix_registry_failure(self, module_name):
        """Advanced registry failure recovery"""
        print(f"🔧 REGISTRY RECOVERY: {module_name}")
        
        # Strategy 1: Install with --no-demo-data
        try:
            result = subprocess.run([
                'docker', 'exec', 'odoo_test_instance',
                'odoo', '-d', 'cbms_test_db', '--db_host=odoo_test_db',
                '--db_user=odoo', '--db_password=odoo',
                '-i', module_name, '--without-demo=all', '--stop-after-init'
            ], capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print(f"  ✅ SUCCESS with --without-demo")
                return True, "SUCCESS_NO_DEMO"
        except:
            pass
        
        # Strategy 2: Install with database update
        try:
            result = subprocess.run([
                'docker', 'exec', 'odoo_test_instance',
                'odoo', '-d', 'cbms_test_db', '--db_host=odoo_test_db',
                '--db_user=odoo', '--db_password=odoo',
                '-i', module_name, '--update=all', '--stop-after-init'
            ], capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print(f"  ✅ SUCCESS with --update=all")
                return True, "SUCCESS_UPDATE"
        except:
            pass
        
        # Strategy 3: Force install with init
        try:
            result = subprocess.run([
                'docker', 'exec', 'odoo_test_instance',
                'odoo', '-d', 'cbms_test_db', '--db_host=odoo_test_db',
                '--db_user=odoo', '--db_password=odoo',
                '-i', module_name, '--init', module_name, '--stop-after-init'
            ], capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print(f"  ✅ SUCCESS with --init")
                return True, "SUCCESS_INIT"
        except:
            pass
        
        print(f"  ❌ REGISTRY RECOVERY FAILED")
        return False, "REGISTRY_RECOVERY_FAILED"
    
    def fix_xml_structure(self, module_name):
        """Fix XML structure issues"""
        print(f"🔧 XML STRUCTURE FIX: {module_name}")
        
        # Check if module has XML issues and try to fix
        module_path = Path(module_name)
        if not module_path.exists():
            return False, "MODULE_NOT_FOUND"
        
        # Look for XML files with potential issues
        xml_files = list(module_path.rglob("*.xml"))
        
        for xml_file in xml_files:
            try:
                content = xml_file.read_text()
                # Basic XML structure fixes
                if 'extra content: record' in content:
                    # Try to fix common XML structure issues
                    fixed_content = self.fix_xml_content(content)
                    if fixed_content != content:
                        # Backup original
                        backup_file = xml_file.with_suffix('.xml.backup')
                        xml_file.rename(backup_file)
                        xml_file.write_text(fixed_content)
                        print(f"  🔧 Fixed XML structure in {xml_file}")
            except Exception as e:
                print(f"  ⚠️ Could not fix {xml_file}: {e}")
        
        # Try installation after fixes
        return self.try_standard_install(module_name)
    
    def fix_xml_content(self, content):
        """Apply common XML fixes"""
        # Remove extra record tags that might be causing issues
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Skip lines that might cause "extra content" issues
            if 'record' in line and 'extra content' in line:
                continue
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_database_conflict(self, module_name):
        """Fix database conflict issues"""
        print(f"🔧 DATABASE CONFLICT FIX: {module_name}")
        
        # Strategy: Clear conflicting data first
        try:
            # Clear module-specific data
            subprocess.run([
                'docker', 'exec', '-e', 'PGPASSWORD=odoo', 'odoo_test_instance',
                'psql', '-h', 'odoo_test_db', '-U', 'odoo', '-d', 'cbms_test_db',
                '-c', f"DELETE FROM ir_module_module WHERE name='{module_name}';"
            ], capture_output=True, text=True, timeout=30)
            
            # Try fresh installation
            return self.try_standard_install(module_name)
            
        except Exception as e:
            print(f"  ❌ Database conflict fix failed: {e}")
            return False, "DB_CONFLICT_FIX_FAILED"
    
    def fix_dependency_missing(self, module_name):
        """Fix missing dependency issues"""
        print(f"🔧 DEPENDENCY FIX: {module_name}")
        
        # Check manifest for dependencies
        manifest_path = Path(module_name) / '__manifest__.py'
        if not manifest_path.exists():
            return False, "NO_MANIFEST"
        
        try:
            with open(manifest_path, 'r') as f:
                manifest_content = f.read()
            
            # Extract dependencies
            import ast
            try:
                manifest_dict = ast.literal_eval(manifest_content)
                depends = manifest_dict.get('depends', [])
                
                # Try to install dependencies first
                for dep in depends:
                    if dep not in ['base', 'web']:  # Skip core modules
                        print(f"  📦 Installing dependency: {dep}")
                        self.try_standard_install(dep)
                
                # Now try the main module
                return self.try_standard_install(module_name)
                
            except:
                # If manifest parsing fails, try standard install
                return self.try_standard_install(module_name)
                
        except Exception as e:
            print(f"  ❌ Dependency fix failed: {e}")
            return False, "DEPENDENCY_FIX_FAILED"
    
    def try_standard_install(self, module_name):
        """Standard installation attempt"""
        try:
            result = subprocess.run([
                'docker', 'exec', 'odoo_test_instance',
                'odoo', '-d', 'cbms_test_db', '--db_host=odoo_test_db',
                '--db_user=odoo', '--db_password=odoo',
                '-i', module_name, '--stop-after-init'
            ], capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                return True, "SUCCESS_STANDARD"
            else:
                return False, "STANDARD_INSTALL_FAILED"
        except Exception as e:
            return False, f"INSTALL_ERROR: {str(e)}"
    
    def run_recovery_session(self):
        """Run comprehensive recovery session"""
        print("🚀 ZOE 100x ENGINEER - ADVANCED RECOVERY SESSION")
        print("=" * 80)
        print(f"🎯 TARGETING {len(self.failed_modules)} FAILED MODULES FOR RECOVERY")
        print("=" * 80)
        
        recovered_modules = []
        still_failed = []
        
        for i, failed_module in enumerate(self.failed_modules, 1):
            module_name = failed_module['module']
            error_msg = failed_module['error']
            
            print(f"\n[{i:3d}/{len(self.failed_modules)}] RECOVERING: {module_name}")
            print(f"  📋 Original Error: {error_msg[:100]}...")
            
            # Categorize and apply targeted recovery
            failure_type = self.categorize_failure(error_msg)
            print(f"  🔍 Failure Type: {failure_type}")
            
            if failure_type in self.recovery_strategies:
                success, result = self.recovery_strategies[failure_type](module_name)
                
                if success:
                    recovered_modules.append({
                        'module': module_name,
                        'recovery_method': result,
                        'original_error': error_msg
                    })
                    self.success_count += 1
                    print(f"  ✅ RECOVERED: {module_name} ({result})")
                else:
                    still_failed.append({
                        'module': module_name,
                        'recovery_attempt': result,
                        'original_error': error_msg
                    })
                    print(f"  ❌ STILL FAILED: {module_name} ({result})")
            else:
                # Try standard recovery for unknown failures
                success, result = self.try_standard_install(module_name)
                if success:
                    recovered_modules.append({
                        'module': module_name,
                        'recovery_method': 'UNKNOWN_TYPE_STANDARD',
                        'original_error': error_msg
                    })
                    self.success_count += 1
                    print(f"  ✅ RECOVERED: {module_name} (STANDARD)")
                else:
                    still_failed.append({
                        'module': module_name,
                        'recovery_attempt': 'UNKNOWN_TYPE_FAILED',
                        'original_error': error_msg
                    })
                    print(f"  ❌ STILL FAILED: {module_name}")
            
            # Progress update every 25 modules
            if i % 25 == 0:
                recovery_rate = (len(recovered_modules) / i) * 100
                print(f"\n📊 RECOVERY CHECKPOINT - Progress: {i}/{len(self.failed_modules)}")
                print(f"✅ Recovered: {len(recovered_modules)}")
                print(f"❌ Still Failed: {len(still_failed)}")
                print(f"📈 Recovery Rate: {recovery_rate:.1f}%")
                print()
            
            # Brief pause between modules
            time.sleep(0.5)
        
        # Final comprehensive report
        self.generate_recovery_report(recovered_modules, still_failed)
        
        return len(recovered_modules), len(still_failed)
    
    def generate_recovery_report(self, recovered, still_failed):
        """Generate comprehensive recovery report"""
        print("\n" + "=" * 80)
        print("📋 ZOE 100x ENGINEER - ADVANCED RECOVERY COMPLETE")
        print("=" * 80)
        
        total_attempted = len(recovered) + len(still_failed)
        recovery_rate = (len(recovered) / total_attempted * 100) if total_attempted > 0 else 0
        
        print(f"📊 Recovery Session Results:")
        print(f"  🎯 Total modules attempted: {total_attempted}")
        print(f"  ✅ Successfully recovered: {len(recovered)}")
        print(f"  ❌ Still failed: {len(still_failed)}")
        print(f"  📈 Recovery success rate: {recovery_rate:.1f}%")
        
        # Calculate new overall project status
        original_successful = 153  # From previous session
        new_total_successful = original_successful + len(recovered)
        total_project_modules = 491
        new_overall_rate = (new_total_successful / total_project_modules) * 100
        
        print(f"\n🎯 UPDATED OVERALL PROJECT STATUS:")
        print(f"  📊 Total project modules: {total_project_modules}")
        print(f"  ✅ Total successfully installed: {new_total_successful}")
        print(f"  📈 New overall success rate: {new_overall_rate:.1f}%")
        
        if len(recovered) > 0:
            print(f"\n✅ NEWLY RECOVERED MODULES ({len(recovered)}):")
            for module in recovered[:20]:  # Show first 20
                print(f"  • {module['module']} ({module['recovery_method']})")
            if len(recovered) > 20:
                print(f"  ... and {len(recovered) - 20} more recovered modules")
        
        # Save detailed results
        recovery_results = {
            "recovery_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_attempted": total_attempted,
            "recovered_modules": recovered,
            "still_failed_modules": still_failed,
            "recovery_success_rate": recovery_rate,
            "new_overall_success_rate": new_overall_rate,
            "new_total_successful": new_total_successful
        }
        
        with open('zoe_advanced_recovery_results.json', 'w') as f:
            json.dump(recovery_results, f, indent=2)
        
        print(f"\n📄 Detailed recovery results saved to zoe_advanced_recovery_results.json")
        
        # Achievement levels
        if new_overall_rate >= 50:
            print("\n🏆 MAJOR BREAKTHROUGH: 50%+ MODULES INSTALLED!")
        elif new_overall_rate >= 40:
            print("\n🏆 SIGNIFICANT PROGRESS: 40%+ MODULES INSTALLED!")
        elif recovery_rate >= 25:
            print("\n👍 GOOD RECOVERY: 25%+ of failed modules recovered!")
        
        print("\n🎉 ZOE 100x ENGINEER ADVANCED RECOVERY SESSION COMPLETE!")

def main():
    recovery_system = ZoeAdvancedRecovery()
    recovered_count, still_failed_count = recovery_system.run_recovery_session()
    
    print(f"\n🎯 FINAL RECOVERY RESULTS:")
    print(f"✅ Recovered: {recovered_count} modules")
    print(f"❌ Still Failed: {still_failed_count} modules")
    
    if recovered_count > 50:
        print("🏆 EXCELLENT RECOVERY PERFORMANCE!")
    elif recovered_count > 25:
        print("👍 GOOD RECOVERY PERFORMANCE!")
    else:
        print("🔄 RECOVERY ATTEMPTED - CONTINUING ANALYSIS")

if __name__ == "__main__":
    main()
