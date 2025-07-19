#!/usr/bin/env python3
"""
Test next batch of modules starting from where we left off
"""
import os
import subprocess
import time

def get_module_list():
    """Get list of available modules"""
    modules = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, '__manifest__.py')):
            modules.append(item)
    
    excluded = ['config', 'logs', '__pycache__', '.git', '.github']
    modules = [m for m in modules if m not in excluded and not m.startswith('.')]
    return sorted(modules)

def test_module(module_name):
    """Test a single module installation"""
    print(f"\n🔧 Testing module: {module_name}")
    
    try:
        result = subprocess.run([
            "docker", "exec", "odoo_test_instance",
            "odoo", "-d", "cbms_test_db",
            "-i", module_name,
            "--stop-after-init"
        ], capture_output=True, text=True, timeout=120)
        
        success = result.returncode == 0
        
        if success:
            print(f"✅ {module_name} - SUCCESS")
        else:
            print(f"❌ {module_name} - FAILED")
            # Show last few lines of stderr for debugging
            if result.stderr:
                error_lines = result.stderr.split('\n')[-5:]
                for line in error_lines:
                    if line.strip() and ('ERROR' in line or 'Exception' in line):
                        print(f"   Error: {line.strip()}")
        
        return success, result.stderr
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {module_name} - TIMEOUT")
        return False, "Installation timeout"
    except Exception as e:
        print(f"❌ {module_name} - EXCEPTION: {e}")
        return False, str(e)

def main():
    """Test next batch of modules"""
    print("🧪 TESTING NEXT BATCH OF MODULES")
    print("=" * 50)
    
    modules = get_module_list()
    
    # Skip the first 10 we already tested, test next 15
    start_idx = 10
    end_idx = 25
    test_modules = modules[start_idx:end_idx]
    
    print(f"Testing modules {start_idx+1}-{end_idx}:")
    for i, module in enumerate(test_modules, start_idx+1):
        print(f"   {i}. {module}")
    
    print("=" * 50)
    
    results = []
    failed_modules = []
    
    for i, module in enumerate(test_modules, start_idx+1):
        print(f"\n[{i}/{end_idx}] Testing: {module}")
        success, error = test_module(module)
        
        results.append({
            'module': module,
            'success': success,
            'error': error
        })
        
        if not success:
            failed_modules.append(module)
        
        time.sleep(1)  # Small delay between tests
    
    # Summary
    successful = len([r for r in results if r['success']])
    total = len(results)
    
    print("\n" + "=" * 50)
    print("📊 BATCH TEST RESULTS")
    print("=" * 50)
    print(f"Total tested: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(failed_modules)}")
    print(f"Success rate: {(successful/total*100):.1f}%")
    
    if failed_modules:
        print(f"\n❌ Failed modules:")
        for module in failed_modules:
            print(f"   - {module}")
    
    return results

if __name__ == "__main__":
    main()
