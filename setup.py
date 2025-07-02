#!/usr/bin/env python3
"""
Simple Setup Script

just installs stuff so that it works
"""

import subprocess
import sys
import os
import platform

def print_step(step_num, description):
    """Print what step we're on"""
    print(f"\n--- Step {step_num}: {description} ---")

def check_python():
    """Make sure Python version is good enough"""
    print("Checking Python version...")
    
    version = sys.version_info
    print(f"Your Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("* Python version is good!")
        return True
    else:
        print("X You need Python 3.8 or newer")
        print("Download from: https://python.org")
        return False

def install_packages():
    """Install the Python packages we need"""
    print("Installing required packages...")
    
    # List of packages we need
    packages = [
        "requests",
        "beautifulsoup4", 
        "pandas",
        "lxml"
    ]
    
    failed = []
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL)
            print(f"* {package} installed")
        except:
            print(f"X Failed to install {package}")
            failed.append(package)
    
    if failed:
        print(f"\nSome packages failed: {failed}")
        print("Try running this command manually:")
        print(f"pip install {' '.join(failed)}")
        return False
    
    print("* All packages installed!")
    return True

def test_imports():
    """Test if we can import the packages we need"""
    print("Testing if packages work...")
    
    packages_to_test = [
        ('requests', 'requests'),
        ('BeautifulSoup', 'bs4'),
        ('pandas', 'pandas')
    ]
    
    all_good = True
    
    for name, import_name in packages_to_test:
        try:
            __import__(import_name)
            print(f"* {name} works")
        except ImportError:
            print(f"X {name} not working")
            all_good = False
    
    return all_good

def create_folders():
    """Create folders we'll need for the project"""
    print("Creating project folders...")
    
    folders = ['data', 'reports']
    
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"* Created {folder}/ folder")
        except:
            print(f"WARNING: Could not create {folder}/ folder")

def create_gitignore():
    """Create .gitignore so we don't accidentally commit data files"""
    print("Creating .gitignore file...")
    
    gitignore_content = """
# Don't commit data files
*.csv
*.json
data/
reports/

# Don't commit Python cache
__pycache__/
*.pyc

# Don't commit API keys
.env
*_key.txt

# Don't commit IDE files
.vscode/
.idea/
"""
    
    try:
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content.strip())
        print("* Created .gitignore")
    except:
        print("WARNING: Could not create .gitignore")

def test_basic_scraping():
    """Test if basic web scraping works"""
    print("Testing basic web scraping...")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Test with a simple website
        response = requests.get('https://httpbin.org/html', timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if soup.find('h1'):
            print("* Basic web scraping works!")
            return True
        else:
            print("WARNING: Web scraping might have issues")
            return False
            
    except Exception as e:
        print(f"X Web scraping test failed: {e}")
        return False

def main():
    """Run the complete setup"""
    print("=== Job Matching System Setup ===")
    print("This will set up your computer for the project")
    
    # Ask if user wants to continue
    response = input("\nProceed with setup? (y/n): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Setup cancelled")
        return
    
    success_count = 0
    total_steps = 6
    
    # Step 1: Check Python
    print_step(1, "Check Python Version")
    if check_python():
        success_count += 1
    
    # Step 2: Install packages
    print_step(2, "Install Required Packages")
    if install_packages():
        success_count += 1
    
    # Step 3: Test imports
    print_step(3, "Test Package Imports")
    if test_imports():
        success_count += 1
    
    # Step 4: Create folders
    print_step(4, "Create Project Folders")
    create_folders()
    success_count += 1  # This usually works
    
    # Step 5: Create .gitignore
    print_step(5, "Create .gitignore File")
    create_gitignore()
    success_count += 1  # This usually works
    
    # Step 6: Test scraping
    print_step(6, "Test Web Scraping")
    if test_basic_scraping():
        success_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"SETUP SUMMARY")
    print(f"{'='*50}")
    print(f"Completed: {success_count}/{total_steps} steps")
    
    if success_count == total_steps:
        print(" Setup complete! You're ready to go!")
        print("\nNext steps:")
        print("1. Run: python job_scraper.py")
        print("2. Or run: python stage1_complete.py")
    elif success_count >= 4:
        print("* Setup mostly successful!")
        print("You should be able to run the project")
    else:
        print("X Setup had issues")
        print("Try fixing the errors above before proceeding")
    
    print(f?"\n Project files you should have:")
    files_needed = [
        'job_scraper.py',
        'api_scraper.py', 
        'data_validator.py',
        'config.py',
        'stage1_complete.py'
    ]
    
    for file in files_needed:
        if os.path.exists(file):
            print(f"* {file}")
        else:
            print(f"X {file} (missing)")

if __name__ == "__main__":
    main()