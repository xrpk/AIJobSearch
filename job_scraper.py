#!/usr/bin/env python3
"""
Ryan Krell
Job Scraper 
Stage 1: Basic web scraping with BeautifulSoup

A straightforward job scraper that collects job postings from Indeed
with basic error handling and ethical considerations.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random
from datetime import datetime
import pandas as pd

class SimpleJobScraper:
    def __init__(self, location="St. Louis, MO", keywords="computer science"):
        self.location = location
        self.keywords = keywords
        self.jobs = []
        
        # Simple headers to look like a regular browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def check_robots_txt(self, website_url):
        """
        Check if we're allowed to scrape (basic check)
        """
        try:
            robots_url = website_url + "/robots.txt"
            response = requests.get(robots_url, timeout=5)
            print(f"Checking robots.txt for {website_url}:")
            print("-" * 40)
            print(response.text[:500])  # Show first 500 characters
            print("-" * 40)
            return True
        except:
            print(f"Could not check robots.txt for {website_url}")
            return False
    
    def scrape_indeed(self, max_pages=3):
        """
        Scrape job postings from Indeed
        """
        print(f"Scraping Indeed for '{self.keywords}' jobs in {self.location}")
        
        # Check robots.txt first
        self.check_robots_txt("https://indeed.com")
        
        for page in range(max_pages):
            print(f"Scraping page {page + 1}...")
            
            # Build the search URL
            url = "https://indeed.com/jobs"
            params = {
                'q': self.keywords,
                'l': self.location,
                'start': page * 10
            }
            
            try:
                # Make the request
                response = requests.get(url, params=params, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards (this might need updating if Indeed changes their HTML)
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                if not job_cards:
                    print("No job cards found - website structure might have changed")
                    break
                
                # Extract info from each job card
                for card in job_cards:
                    try:
                        # Get job title
                        title_element = card.find('h2', class_='jobTitle')
                        title = title_element.get_text().strip() if title_element else "No Title"
                        
                        # Get company name
                        company_element = card.find('span', class_='companyName')
                        company = company_element.get_text().strip() if company_element else "No Company"
                        
                        # Get location
                        location_element = card.find('div', class_='companyLocation')
                        location = location_element.get_text().strip() if location_element else "No Location"
                        
                        # Get job description/summary
                        summary_element = card.find('div', class_='summary')
                        description = summary_element.get_text().strip() if summary_element else "No Description"
                        
                        # Get job URL (if available)
                        link_element = title_element.find('a') if title_element else None
                        job_url = "https://indeed.com" + link_element.get('href') if link_element and link_element.get('href') else "No URL"
                        
                        # Store the job data
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': location,
                            'description': description,
                            'url': job_url,
                            'source': 'Indeed',
                            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        self.jobs.append(job_data)
                        print(f"Found: {title} at {company}")
                        
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                
                # Be nice to the website - wait between requests
                wait_time = random.uniform(2, 4)  # Wait 2-4 seconds
                print(f"Waiting {wait_time:.1f} seconds before next page...")
                time.sleep(wait_time)
                
            except Exception as e:
                print(f"Error scraping page {page + 1}: {e}")
                break
        
        print(f"Finished scraping. Found {len(self.jobs)} jobs total.")
        return self.jobs
    
    def save_to_csv(self, filename="job_postings.csv"):
        """
        Save jobs to CSV file
        """
        if not self.jobs:
            print("No jobs to save!")
            return
        
        try:
            df = pd.DataFrame(self.jobs)
            df.to_csv(filename, index=False)
            print(f"Saved {len(self.jobs)} jobs to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def save_to_json(self, filename="job_postings.json"):
        """
        Save jobs to JSON file
        """
        if not self.jobs:
            print("No jobs to save!")
            return
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.jobs, f, indent=2)
            print(f"Saved {len(self.jobs)} jobs to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def print_sample_jobs(self, num_samples=3):
        """
        Print a few sample jobs to see what we collected
        """
        if not self.jobs:
            print("No jobs to display!")
            return
        
        print(f"\nSample jobs (showing first {num_samples}):")
        print("=" * 60)
        
        for i, job in enumerate(self.jobs[:num_samples]):
            print(f"\nJob {i+1}:")
            print(f"Title: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Description: {job['description'][:100]}...")  # First 100 characters
            print("-" * 40)

def main():
    """
    Main function to run the scraper
    """
    print("=== Simple Job Scraper ===")
    print("This will scrape computer science jobs from Indeed in St. Louis")
    
    # Create scraper
    scraper = SimpleJobScraper(
        location="St. Louis, MO",
        keywords="computer science software developer"
    )
    
    # Scrape jobs
    jobs = scraper.scrape_indeed(max_pages=2)  # Just 2 pages to start
    
    if jobs:
        # Show some sample jobs
        scraper.print_sample_jobs()
        
        # Save the data
        scraper.save_to_csv()
        scraper.save_to_json()
        
        print(f"\n Success! Collected {len(jobs)} job postings")
        print("Files created:")
        print("  - job_postings.csv")
        print("  - job_postings.json")
    else:
        print("No jobs were collected. Try checking your internet connection or the website structure.")

if __name__ == "__main__":
    main()