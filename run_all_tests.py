#!/usr/bin/env python3
"""
just for testing 

change test_file 


"""

import os
import sys
import subprocess
import pandas as pd

def print_test(test_name):
    """Print test header"""
    print(f"\n{'='*50}")
    print(f"TEST: {test_name}")
    print('='*50)

def test_import():
    """Test 1: Can we import our modules?"""
    print_test("Import Test")
    
    try:
        from data_preprocessor import SimpleJobCleaner, ResumeTextCleaner
        print(" Import successful!")
        return True
    except Exception as e:
        print(f" Import failed: {e}")
        return False

def test_sample_data():
    """Test 2: Run the test script"""
    print_test("Sample Data Test")
    
    try:
        result = subprocess.run([sys.executable, 'test_stage2.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(" test_stage2.py ran successfully!")
            print("Output:")
            print(result.stdout[-500:])  # Last 500 characters
            return True
        else:
            print(f" test_stage2.py failed!")
            print("Error:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("Test timed out (took too long)")
        return False
    except Exception as e:
        print(f" Error running test: {e}")
        return False

def test_output_files():
    """Test 3: Check if test files were created"""
    print_test("Output Files Test")
    
    expected_files = [
        'test_jobs.csv',
        'test_clean_jobs.csv', 
        'test_clean_resume.txt'
    ]
    
    all_good = True
    
    for filename in expected_files:
        if os.path.exists(filename):
            print(f" {filename} exists")
            
            # Check file size
            size = os.path.getsize(filename)
            if size > 0:
                print(f"   Size: {size} bytes")
            else:
                print(f"    File is empty")
                all_good = False
        else:
            print(f" {filename} missing")
            all_good = False
    
    return all_good

def test_csv_structure():
    """Test 4: Check CSV file structure"""
    print_test("CSV Structure Test")
    
    test_file = 'test_clean_jobs.csv'
    
    if not os.path.exists(test_file):
        print(f" {test_file} doesn't exist")
        return False
    
    try:
        df = pd.read_csv(test_file)
        print(f" CSV loads successfully")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        
        # Check for required columns
        required_cols = ['title', 'company', 'location', 'description', 'clean_text']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f" Missing columns: {missing_cols}")
            return False
        else:
            print(" All required columns present")
        
        # Check clean_text column
        if 'clean_text' in df.columns:
            sample_text = df['clean_text'].iloc[0] if len(df) > 0 else ""
            print(f"   Sample clean_text: {sample_text[:100]}...")
            
            if len(sample_text) > 10:
                print(" clean_text looks good")
            else:
                print("clean_text seems too short")
        
        return True
        
    except Exception as e:
        print(f" Error reading CSV: {e}")
        return False

def test_real_data():
    """Test 5: Try with real Stage 1 data if available"""
    print_test("Real Data Test (Optional)")
    
    # Look for Stage 1 output files
    possible_files = []
    for filename in os.listdir('.'):
        if filename.endswith('.csv') and ('job' in filename.lower() or 'final' in filename.lower()):
            if 'test' not in filename.lower() and 'clean' not in filename.lower():
                possible_files.append(filename)
    
    if not possible_files:
        print(" No Stage 1 data files found")
        print("   This is OK if you haven't run Stage 1 yet")
        return True
    
    print(f"Found possible Stage 1 files: {possible_files}")
    
    # Try the first one
    test_file = possible_files[0]
    print(f"Testing with: {test_file}")
    
    try:
        from data_preprocessor import SimpleJobCleaner
        
        cleaner = SimpleJobCleaner()
        if cleaner.load_jobs(test_file):
            print(f"Loaded {len(cleaner.jobs_data)} jobs from {test_file}")
            
            # Try cleaning a few jobs
            if len(cleaner.jobs_data) > 0:
                cleaned = cleaner.clean_all_jobs()
                if cleaned is not None and len(cleaned) > 0:
                    print(f" Cleaned {len(cleaned)} jobs successfully")
                    return True
                else:
                    print(" Cleaning failed or no jobs left")
                    return False
            else:
                print(" No jobs in file")
                return True
        else:
            print(f"" Couldn't load {test_file}")
            return False
            
    except Exception as e:
        print(f"Error testing real data: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    print_test("Cleanup")
    
    test_files = [
        'test_jobs.csv',
        'test_clean_jobs.csv',
        'test_clean_resume.txt'
    ]
    
    for filename in test_files:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"Removed {filename}")
            except:
                print(f" Couldn't remove {filename}")

def main():
    """Run all tests"""
    print("STAGE 2 TEST RUNNER")
    print("Running tests before merging to main branch")
    
    tests = [
        ("Import Test", test_import),
        ("Sample Data Test", test_sample_data),
        ("Output Files Test", test_output_files),
        ("CSV Structure Test", test_csv_structure),
        ("Real Data Test", test_real_data),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f" {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST RESULTS SUMMARY")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\ ALL TESTS PASSED!")
        print("Stage 2 is ready to merge to main branch")
        print("\nNext steps:")
        print("1. git add .")
        print("2. git commit -m 'Stage 2 ready for merge'")
        print("3. git push origin feature/stage2-preprocessing")
        print("4. Create pull request or merge to main")
    else:
        print(f"\ {total - passed} TESTS FAILED")
        print("Fix the issues before merging to main")
    
    # Ask about cleanup
    print(f"\nClean up test files? (y/n): ", end="")
    if input().lower().startswith('y'):
        cleanup_test_files()

if __name__ == "__main__":
    main()