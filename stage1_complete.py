#!/usr/bin/env python3
"""
Complete Stage 1: Run Everything Together
Simple pipeline that runs web scraping, API collection, and data validation

This script runs all the Stage 1 components together to collect
job data and check its quality.
"""

import os
from datetime import datetime
import pandas as pd
import json

# Import our other modules
try:
    from job_scraper import SimpleJobScraper
    from api_scraper import SimpleAPICollector  
    from data_validator import SimpleDataChecker
except ImportError:
    print("❌ Error: Make sure all files are in the same directory!")
    print("Required files: job_scraper.py, api_scraper.py, data_validator.py")
    exit(1)

def print_header(text):
    """Print a nice header"""
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")

def step1_web_scraping():
    """
    Step 1: Collect jobs using web scraping
    """
    print_header("STEP 1: WEB SCRAPING")
    
    print("Collecting jobs from Indeed...")
    
    # Create scraper
    scraper = SimpleJobScraper(
        location="St. Louis, MO",
        keywords="computer science software developer"
    )
    
    # Scrape jobs (just 2 pages to keep it reasonable)
    scraped_jobs = scraper.scrape_indeed(max_pages=2)
    
    if scraped_jobs:
        print(f"✅ Web scraping completed! Found {len(scraped_jobs)} jobs")
        
        # Save scraped jobs
        scraper.save_to_csv("scraped_jobs.csv")
        return scraped_jobs
    else:
        print("⚠️ No jobs found from web scraping")
        return []

def step2_api_collection():
    """
    Step 2: Collect jobs using APIs
    """
    print_header("STEP 2: API COLLECTION")
    
    print("Collecting jobs from APIs...")
    
    # Create API collector
    collector = SimpleAPICollector(
        location="St. Louis, MO", 
        keywords="software developer computer science"
    )
    
    # Add your RapidAPI key here if you have one
    rapidapi_key = None  # Replace with "your_api_key_here" if you have one
    
    # Collect from APIs
    api_jobs = collector.collect_all_jobs(rapidapi_key)
    
    if api_jobs:
        print(f"✅ API collection completed! Found {len(api_jobs)} jobs")
        
        # Save API jobs
        collector.save_data()
        return api_jobs
    else:
        print("⚠️ No jobs found from APIs")
        return []

def step3_combine_data(scraped_jobs, api_jobs):
    """
    Step 3: Combine all job data and remove duplicates
    """
    print_header("STEP 3: COMBINING DATA")
    
    print("Combining web scraped and API jobs...")
    
    # Combine all jobs
    all_jobs = scraped_jobs + api_jobs
    
    if not all_jobs:
        print("❌ No jobs to combine!")
        return []
    
    print(f"Total jobs before removing duplicates: {len(all_jobs)}")
    
    # Simple duplicate removal based on title + company
    unique_jobs = []
    seen_jobs = set()
    duplicates_removed = 0
    
    for job in all_jobs:
        # Create a simple identifier
        job_id = (job['title'].lower().strip(), job['company'].lower().strip())
        
        if job_id not in seen_jobs and job_id != ('', ''):
            seen_jobs.add(job_id)
            unique_jobs.append(job)
        else:
            duplicates_removed += 1
    
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final unique jobs: {len(unique_jobs)}")
    
    # Save combined data
    if unique_jobs:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to CSV
        df = pd.DataFrame(unique_jobs)
        csv_filename = f"final_jobs_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        
        # Save to JSON  
        json_filename = f"final_jobs_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(unique_jobs, f, indent=2)
        
        print(f"✅ Combined data saved to:")
        print(f"  - {csv_filename}")
        print(f"  - {json_filename}")
        
        return unique_jobs, csv_filename
    else:
        print("❌ No unique jobs to save!")
        return [], None

def step4_quality_check(data_filename):
    """
    Step 4: Check the quality of our collected data
    """
    print_header("STEP 4: QUALITY CHECK")
    
    if not data_filename:
        print("❌ No data file to check!")
        return
    
    print(f"Checking quality of {data_filename}...")
    
    # Create data checker
    checker = SimpleDataChecker()
    
    if checker.load_data(data_filename):
        # Run quality check
        checker.generate_simple_report()
        return True
    else:
        print("❌ Could not check data quality")
        return False

def step5_summary(scraped_count, api_count, final_count):
    """
    Step 5: Show final summary
    """
    print_header("STAGE 1 COMPLETE!")
    
    print("📊 FINAL RESULTS:")
    print(f"  Web scraped jobs: {scraped_count}")
    print(f"  API collected jobs: {api_count}")
    print(f"  Total collected: {scraped_count + api_count}")
    print(f"  Final unique jobs: {final_count}")
    
    if final_count >= 20:
        print("\n🎉 SUCCESS! You have plenty of job data for Stage 2!")
    elif final_count >= 10:
        print("\n✅ Good! You have enough data to proceed to Stage 2.")
    else:
        print("\n⚠️ You might want to collect more data before Stage 2.")
    
    print(f"\n📁 FILES CREATED:")
    print(f"  - scraped_jobs.csv (web scraped data)")
    print(f"  - api_jobs_*.csv (API collected data)")
    print(f"  - final_jobs_*.csv (combined & cleaned data)")
    print(f"  - final_jobs_*.json (same data in JSON format)")
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"  1. Review the quality report above")
    print(f"  2. If quality looks good, proceed to Stage 2 (Data Preprocessing)")
    print(f"  3. Stage 2 will clean the text and prepare it for embeddings")
    
    print(f"\n💡 TIPS FOR STAGE 2:")
    print(f"  - Use the final_jobs_*.csv file as input")
    print(f"  - You'll also need to prepare your resume text")
    print(f"  - Stage 2 will clean job descriptions and extract key information")

def main():
    """
    Main function that runs the complete Stage 1 pipeline
    """
    print("🎯 JOB MATCHING SYSTEM - STAGE 1: DATA ACQUISITION")
    print("This will collect job data using web scraping and APIs")
    
    # Ask user if they want to proceed
    print("\nThis will:")
    print("1. Scrape jobs from Indeed (2 pages)")
    print("2. Collect jobs from free APIs") 
    print("3. Combine and remove duplicates")
    print("4. Check data quality")
    
    response = input("\nProceed? (y/n): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Initialize counters
    scraped_jobs = []
    api_jobs = []
    final_jobs = []
    data_filename = None
    
    try:
        # Step 1: Web scraping
        scraped_jobs = step1_web_scraping()
        
        # Step 2: API collection
        api_jobs = step2_api_collection()
        
        # Step 3: Combine data
        final_jobs, data_filename = step3_combine_data(scraped_jobs, api_jobs)
        
        # Step 4: Quality check
        if data_filename:
            step4_quality_check(data_filename)
        
        # Step 5: Final summary
        step5_summary(len(scraped_jobs), len(api_jobs), len(final_jobs))
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopped by user")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Check that all required files are in the same directory")
    
    print(f"\n{'='*60}")
    print("Stage 1 pipeline finished!")

if __name__ == "__main__":
    main()