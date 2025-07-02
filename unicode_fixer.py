#!/usr/bin/env python3
"""
Unicode Character Fixer
Removes emoji and Unicode characters that cause issues on Windows

Run this script to fix Unicode issues in your Python files.
"""

import os
import re

def fix_unicode_in_file(filename):
    """
    Remove problematic Unicode characters from a Python file
    """
    if not os.path.exists(filename):
        print(f"File {filename} not found, skipping...")
        return False
    
    try:
        # Read the file
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Store original content to check if changes were made
        original_content = content
        
        # Replace common problematic Unicode characters
        unicode_fixes = {
            '🎯': '',  # Target emoji
            '🚀': '',  # Rocket emoji  
            '💡': '',  # Light bulb emoji
            '🎉': '',  # Party emoji
            '🏆': '',  # Trophy emoji
            '📈': '',  # Chart emoji
            '📊': '',  # Bar chart emoji
            '📝': '',  # Memo emoji
            '🧠': '',  # Brain emoji
            '⚠️': 'WARNING:',  # Warning emoji
            '✅': '*',  # Check mark
            '❌': 'X',  # Cross mark
            '✓': '*',  # Check mark
            '→': '->',  # Arrow
            '•': '*',  # Bullet point
        }
        
        # Apply fixes
        for unicode_char, replacement in unicode_fixes.items():
            content = content.replace(unicode_char, replacement)
        
        # Remove any remaining non-ASCII characters in print statements
        # This regex finds Unicode characters in print statements and removes them
        content = re.sub(r'print\(f?"([^"]*)[^\x00-\x7F]+([^"]*)"', r'print(f?"\1\2"', content)
        content = re.sub(r"print\(f?'([^']*)[^\x00-\x7F]+([^']*)\'", r"print(f?'\1\2'", content)
        
        # Check if any changes were made
        if content != original_content:
            # Write the fixed content back
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed Unicode issues in {filename}")
            return True
        else:
            print(f"No Unicode issues found in {filename}")
            return False
            
    except Exception as e:
        print(f"Error fixing {filename}: {e}")
        return False

def main():
    """
    Main function to fix Unicode issues in project files
    """
    print("=== Unicode Character Fixer ===")
    print("This will remove problematic Unicode characters from your Python files")
    
    # List of files to check and fix
    files_to_fix = [
        'stage1_complete.py',
        'job_scraper.py',
        'api_scraper.py',
        'data_validator.py',
        'llm_embedding_generator.py',
        'local_similarity_matcher.py',
        'local_complete_pipeline.py',
        'setup.py'
    ]
    
    print(f"\nChecking {len(files_to_fix)} files for Unicode issues...")
    
    fixed_count = 0
    for filename in files_to_fix:
        if fix_unicode_in_file(filename):
            fixed_count += 1
    
    print(f"\nSummary:")
    print(f"Files checked: {len(files_to_fix)}")
    print(f"Files fixed: {fixed_count}")
    
    if fixed_count > 0:
        print(f"\nUnicode issues have been fixed!")
        print(f"You can now run your scripts without Unicode errors.")
        print(f"Try running: python local_complete_pipeline.py")
    else:
        print(f"\nNo Unicode issues found in the checked files.")
    
    print(f"\nNote: If you still get Unicode errors, make sure your Windows")
    print(f"command prompt supports UTF-8 encoding, or use an IDE like VS Code.")

if __name__ == "__main__":
    main()