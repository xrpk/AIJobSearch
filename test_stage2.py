#!/usr/bin/env python3
"""
Simple test for Stage 2 preprocessing
Creates fake job data and tests the cleaning

Author: CS Student
"""

import pandas as pd
from data_preprocessor import SimpleJobCleaner, ResumeTextCleaner

def create_test_data():
    """Make some fake messy job data to test with"""
    
    fake_jobs = [
        {
            'title': '   Software Engineer   ',
            'company': 'Google',
            'location': 'St. Louis, MO',
            'description': '<p>We need a <strong>software engineer</strong> with Python skills.</p><br>Equal opportunity employer.',
            'url': 'https://jobs.google.com/1',
            'source': 'Indeed'
        },
        {
            'title': 'Job: Python Developer',
            'company': 'Microsoft',
            'location': 'Saint Louis, Missouri',
            'description': 'No Description',
            'url': 'https://jobs.microsoft.com/1',
            'source': 'API'
        },
        {
            'title': 'Software Engineer',  # This is a duplicate
            'company': 'Google',
            'location': 'St. Louis, MO',
            'description': 'Python developer needed.',
            'url': 'https://jobs.google.com/2',
            'source': 'Scraper'
        },
        {
            'title': 'Web Developer',
            'company': 'Startup XYZ',
            'location': 'KC, MO',
            'description': 'Need web dev with HTML &amp; CSS. Apply now!',
            'url': 'https://startup.com/jobs',
            'source': 'Website'
        },
        {
            'title': '',  # Bad job - no title
            'company': '',
            'location': 'Unknown',
            'description': 'Bad job',
            'url': 'bad.com',
            'source': 'Bad'
        }
    ]
    
    return fake_jobs

def test_job_cleaning():
    """Test the job cleaning"""
    print("=== Testing Job Cleaning ===")
    
    # Create fake data
    fake_jobs = create_test_data()
    df = pd.DataFrame(fake_jobs)
    
    # Save to file
    test_file = "test_jobs.csv"
    df.to_csv(test_file, index=False)
    print(f"Created test file: {test_file}")
    
    # Test the cleaner
    cleaner = SimpleJobCleaner()
    
    if cleaner.load_jobs(test_file):
        print(f"Loaded {len(cleaner.jobs_data)} test jobs")
        
        # Clean the data
        cleaned = cleaner.clean_all_jobs()
        
        if cleaned is not None:
            print(f"Cleaning successful!")
            cleaner.show_samples(2)
            
            # Save results
            output_file = cleaner.save_clean_data("test_clean_jobs.csv")
            print(f"Test results saved to: {output_file}")
            
            return True
    
    return False

def test_resume_cleaning():
    """Test resume cleaning"""
    print("\n=== Testing Resume Cleaning ===")
    
    # Fake resume text
    fake_resume = """
    John Smith
    Software Developer
    
    EXPERIENCE:
    - Python Developer at ABC Corp
    - Web Developer at XYZ Inc
    
    SKILLS: Python, JavaScript, HTML, CSS
    """
    
    cleaner = ResumeTextCleaner()
    
    if cleaner.load_resume(text=fake_resume):
        clean_text = cleaner.clean_resume()
        
        if clean_text:
            print("Resume cleaning successful!")
            print(f"Clean text: {clean_text[:100]}...")
            
            output_file = cleaner.save_clean_resume("test_clean_resume.txt")
            print(f"Test resume saved to: {output_file}")
            
            return True
    
    return False

def main():
    """Run all tests"""
    print("Testing Stage 2 Preprocessing")
    print("This creates fake data and tests the cleaning")
    
    # Test job cleaning
    job_test_ok = test_job_cleaning()
    
    # Test resume cleaning  
    resume_test_ok = test_resume_cleaning()
    
    # Summary
    print(f"\n=== Test Results ===")
    print(f"Job cleaning: {'PASS' if job_test_ok else 'FAIL'}")
    print(f"Resume cleaning: {'PASS' if resume_test_ok else 'FAIL'}")
    
    if job_test_ok and resume_test_ok:
        print("All tests passed! Your Stage 2 is ready.")
        print("Now you can run: python data_preprocessor.py")
    else:
        print("Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()