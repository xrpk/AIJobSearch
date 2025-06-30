#!/usr/bin/env python3
"""
Simple API Job Collector
Stage 1: Collecting jobs using APIs instead of web scraping
"""

import requests
import json
import time
from datetime import datetime
import pandas as pd

class SimpleAPICollector:
    def __init__(self, location="St. Louis, MO", keywords="computer science"):
        self.location = location
        self.keywords = keywords
        self.jobs = []
    
    def get_jobs_from_usajobs(self):
        """
        Get government jobs from USAJobs.gov (no API key needed!)
        """
        print("Getting government jobs from USAJobs.gov...")
        
        url = "https://data.usajobs.gov/api/search"
        
        # USAJobs requires these headers
        headers = {
            'Host': 'data.usajobs.gov',
            'User-Agent': 'student-project@email.com'  # Replace with your email
        }
        
        params = {
            'Keyword': self.keywords,
            'LocationName': self.location,
            'ResultsPerPage': 25
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            data = response.json()
            
            if 'SearchResult' in data and 'SearchResultItems' in data['SearchResult']:
                jobs_found = 0
                for item in data['SearchResult']['SearchResultItems']:
                    job_info = item.get('MatchedObjectDescriptor', {})
                    
                    # Extract job details
                    job_data = {
                        'title': job_info.get('PositionTitle', 'No Title'),
                        'company': job_info.get('OrganizationName', 'U.S. Government'),
                        'location': ', '.join([loc.get('LocationName', '') for loc in job_info.get('PositionLocation', [])]),
                        'description': job_info.get('UserArea', {}).get('Details', {}).get('JobSummary', 'No Description'),
                        'url': job_info.get('PositionURI', 'No URL'),
                        'source': 'USAJobs',
                        'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    self.jobs.append(job_data)
                    jobs_found += 1
                    print(f"Found: {job_data['title']} at {job_data['company']}")
                
                print(f"Got {jobs_found} government jobs")
            else:
                print("No government jobs found")
                
        except Exception as e:
            print(f"Error getting USAJobs data: {e}")
        
        # Be nice to the API
        time.sleep(1)
    
    def get_remote_jobs(self):
        """
        Get remote jobs from RemoteOK (no API key needed!)
        """
        print("Getting remote jobs from RemoteOK...")
        
        url = "https://remoteok.io/api"
        
        headers = {
            'User-Agent': 'Student-Job-Project/1.0'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            data = response.json()
            
            # Skip the first item (it's just metadata)
            remote_jobs = data[1:] if len(data) > 1 else []
            
            jobs_found = 0
            for job in remote_jobs:
                if isinstance(job, dict):
                    # Check if this job matches our keywords
                    title = job.get('position', '').lower()
                    description = job.get('description', '').lower()
                    
                    # Simple keyword matching
                    if any(keyword.lower() in title + ' ' + description 
                           for keyword in self.keywords.split()):
                        
                        job_data = {
                            'title': job.get('position', 'No Title'),
                            'company': job.get('company', 'No Company'),
                            'location': 'Remote',
                            'description': job.get('description', 'No Description'),
                            'url': job.get('url', 'No URL'),
                            'source': 'RemoteOK',
                            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        self.jobs.append(job_data)
                        jobs_found += 1
                        print(f"Found: {job_data['title']} at {job_data['company']}")
                        
                        # Limit to 10 remote jobs so we don't get too many
                        if jobs_found >= 10:
                            break
            
            print(f"Got {jobs_found} remote jobs")
            
        except Exception as e:
            print(f"Error getting RemoteOK data: {e}")
        
        # Be nice to the API
        time.sleep(2)
    
    def get_jobs_with_rapidapi(self, api_key):
        """
        Get jobs using RapidAPI JSearch (requires API key)
        Sign up at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
        """
        if not api_key or api_key == "your_api_key_here":
            print("Skipping RapidAPI - no API key provided")
            print("Get a free API key at: https://rapidapi.com/")
            return
        
        print("Getting jobs from RapidAPI JSearch...")
        
        url = "https://jsearch.p.rapidapi.com/search"
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        params = {
            "query": f"{self.keywords} in {self.location}",
            "page": "1",
            "num_pages": "2"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            data = response.json()
            
            if 'data' in data and data['data']:
                jobs_found = 0
                for job in data['data']:
                    job_data = {
                        'title': job.get('job_title', 'No Title'),
                        'company': job.get('employer_name', 'No Company'),
                        'location': f"{job.get('job_city', '')}, {job.get('job_state', '')}".strip(', '),
                        'description': job.get('job_description', 'No Description'),
                        'url': job.get('job_apply_link', 'No URL'),
                        'source': 'RapidAPI',
                        'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    self.jobs.append(job_data)
                    jobs_found += 1
                    print(f"Found: {job_data['title']} at {job_data['company']}")
                
                print(f"Got {jobs_found} jobs from RapidAPI")
            else:
                print("No jobs found from RapidAPI")
                
        except Exception as e:
            print(f"Error getting RapidAPI data: {e}")
        
        # Be nice to the API
        time.sleep(1)
    
    def collect_all_jobs(self, rapidapi_key=None):
        """
        Collect jobs from all available APIs
        """
        print("Starting API job collection...")
        print(f"Looking for '{self.keywords}' jobs in {self.location}")
        print("-" * 50)
        
        # Get government jobs (always works, no API key needed)
        self.get_jobs_from_usajobs()
        
        # Get remote jobs (no API key needed)
        self.get_remote_jobs()
        
        # Get jobs from RapidAPI (if API key provided)
        if rapidapi_key:
            self.get_jobs_with_rapidapi(rapidapi_key)
        
        # Remove duplicates (simple check by title + company)
        unique_jobs = []
        seen = set()
        
        for job in self.jobs:
            identifier = (job['title'].lower(), job['company'].lower())
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        self.jobs = unique_jobs
        print("-" * 50)
        print(f"Total unique jobs collected: {len(self.jobs)}")
        
        return self.jobs
    
    def save_data(self):
        """
        Save collected jobs to files
        """
        if not self.jobs:
            print("No jobs to save!")
            return
        
        # Save to CSV
        try:
            df = pd.DataFrame(self.jobs)
            csv_filename = f"api_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Saved to {csv_filename}")
        except Exception as e:
            print(f"Error saving CSV: {e}")
        
        # Save to JSON
        try:
            json_filename = f"api_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_filename, 'w') as f:
                json.dump(self.jobs, f, indent=2)
            print(f"Saved to {json_filename}")
        except Exception as e:
            print(f"Error saving JSON: {e}")
    
    def show_sample_jobs(self, num_samples=3):
        """
        Show some sample jobs
        """
        if not self.jobs:
            print("No jobs to show!")
            return
        
        print(f"\nSample jobs (showing first {num_samples}):")
        print("=" * 60)
        
        for i, job in enumerate(self.jobs[:num_samples]):
            print(f"\nJob {i+1}:")
            print(f"Title: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Source: {job['source']}")
            print(f"Description: {job['description'][:100]}...")
            print("-" * 40)

def main():
    """
    Main function to run the API collector
    """
    print("=== Simple API Job Collector ===")
    
    # Create collector
    collector = SimpleAPICollector(
        location="St. Louis, MO",
        keywords="software developer computer science python"
    )
    
    # Option to use RapidAPI (requires free API key)
    # Get your free API key at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
    rapidapi_key = None  # Replace with your API key if you have one
    # rapidapi_key = "your_rapidapi_key_here"
    
    # Collect jobs
    jobs = collector.collect_all_jobs(rapidapi_key)
    
    if jobs:
        # Show sample jobs
        collector.show_sample_jobs()
        
        # Save the data
        collector.save_data()
        
        print(f"\nSuccess! Collected {len(jobs)} job postings via APIs")
    else:
        print("No jobs were collected. Check your internet connection.")

if __name__ == "__main__":
    main()