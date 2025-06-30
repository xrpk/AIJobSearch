#!/usr/bin/env python3
"""
Simple Configuration File
Settings for our job matching system

Just basic settings that we can easily change without 
modifying the main code files.
"""

# Basic search settings
LOCATION = "St. Louis, MO"
KEYWORDS = "computer science software developer python"

# Alternative locations to try if needed
OTHER_LOCATIONS = [
    "Saint Louis, Missouri",
    "St Louis, MO", 
    "Kansas City, MO",
    "Remote"
]

# How many pages to scrape from each site
MAX_PAGES_TO_SCRAPE = 2

# How long to wait between requests (be nice to websites!)
WAIT_TIME_MIN = 2  # minimum seconds
WAIT_TIME_MAX = 4  # maximum seconds

# Required fields that every job posting should have
REQUIRED_FIELDS = [
    'title',
    'company', 
    'location',
    'description',
    'url',
    'source'
]

# File names for saving data
OUTPUT_FILES = {
    'scraped_csv': 'scraped_jobs.csv',
    'api_csv': 'api_jobs.csv',
    'final_csv': 'final_jobs.csv',
    'final_json': 'final_jobs.json'
}

# API settings (add your API keys here if you have them)
API_KEYS = {
    'rapidapi_key': None,  # Get free key at rapidapi.com
    'adzuna_app_id': None,
    'adzuna_app_key': None
}

# Keywords to look for in job titles/descriptions
GOOD_KEYWORDS = [
    'software',
    'developer', 
    'programmer',
    'engineer',
    'python',
    'java',
    'javascript',
    'data scientist',
    'web developer',
    'full stack',
    'backend',
    'frontend'
]

# Keywords to avoid (if we want to filter out certain jobs)
AVOID_KEYWORDS = [
    'unpaid',
    'volunteer',
    'sales'  # Remove this if you want sales jobs
]

# Quality thresholds
QUALITY_SETTINGS = {
    'min_description_length': 50,  # Minimum characters in job description
    'min_jobs_needed': 10,  # Minimum number of jobs we want to collect
    'good_jobs_target': 25,  # Target number of jobs for good dataset
}

# Simple headers for web requests
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Print settings when this file is run
if __name__ == "__main__":
    print("=== Job Matching System Configuration ===")
    print(f"Location: {LOCATION}")
    print(f"Keywords: {KEYWORDS}")
    print(f"Max pages per site: {MAX_PAGES_TO_SCRAPE}")
    print(f"Wait time: {WAIT_TIME_MIN}-{WAIT_TIME_MAX} seconds")
    print(f"Target jobs: {QUALITY_SETTINGS['good_jobs_target']}")
    
    if any(API_KEYS.values()):
        print("✅ API keys configured")
    else:
        print("⚠️ No API keys configured (using free APIs only)")