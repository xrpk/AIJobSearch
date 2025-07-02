#!/usr/bin/env python3
"""
Simple Data Quality Checker
Stage 1: Check if our collected job data is good quality

This script checks the job data we collected to make sure it's complete
and ready for the next stage of our project.

Author: CS Student
Date: 2025
"""

import pandas as pd
import json
from datetime import datetime

class SimpleDataChecker:
    def __init__(self):
        self.data = None
        self.total_jobs = 0
        
    def load_data(self, filename):
        """
        Load our job data from CSV or JSON file
        """
        try:
            if filename.endswith('.csv'):
                self.data = pd.read_csv(filename)
                print(f"* Loaded {len(self.data)} jobs from {filename}")
            elif filename.endswith('.json'):
                with open(filename, 'r') as f:
                    jobs_list = json.load(f)
                self.data = pd.DataFrame(jobs_list)
                print(f"* Loaded {len(self.data)} jobs from {filename}")
            else:
                print("X File must be .csv or .json")
                return False
            
            self.total_jobs = len(self.data)
            return True
            
        except Exception as e:
            print(f"X Error loading file: {e}")
            return False
    
    def check_required_fields(self):
        """
        Check if we have all the important fields
        """
        print("\n=== Checking Required Fields ===")
        
        required_fields = ['title', 'company', 'location', 'description', 'url', 'source']
        missing_fields = []
        
        for field in required_fields:
            if field not in self.data.columns:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"X Missing required fields: {missing_fields}")
            return False
        else:
            print("* All required fields are present")
            return True
    
    def check_data_completeness(self):
        """
        Check how much of our data is complete (not empty)
        """
        print("\n=== Checking Data Completeness ===")
        
        fields_to_check = ['title', 'company', 'location', 'description']
        
        for field in fields_to_check:
            if field in self.data.columns:
                # Count empty, null, or "No X" values
                empty_count = 0
                for value in self.data[field]:
                    if pd.isna(value) or str(value).strip() == '' or str(value).startswith('No '):
                        empty_count += 1
                
                completeness = ((self.total_jobs - empty_count) / self.total_jobs) * 100
                print(f"{field}: {completeness:.1f}% complete ({self.total_jobs - empty_count}/{self.total_jobs})")
                
                if completeness < 80:
                    print(f"  WARNING: Warning: {field} has low completeness")
                else:
                    print(f"  * {field} looks good")
    
    def check_for_duplicates(self):
        """
        Look for duplicate job postings
        """
        print("\n=== Checking for Duplicates ===")
        
        if 'title' in self.data.columns and 'company' in self.data.columns:
            # Check for exact duplicates based on title + company
            duplicates = self.data.duplicated(subset=['title', 'company'], keep=False)
            duplicate_count = duplicates.sum()
            
            if duplicate_count > 0:
                print(f"WARNING: Found {duplicate_count} potential duplicate jobs")
                
                # Show some examples
                duplicate_jobs = self.data[duplicates][['title', 'company']].head(5)
                print("Sample duplicates:")
                for _, job in duplicate_jobs.iterrows():
                    print(f"  - {job['title']} at {job['company']}")
            else:
                print("* No exact duplicates found")
        else:
            print("X Can't check duplicates - missing title or company fields")
    
    def check_job_sources(self):
        """
        See where our jobs came from
        """
        print("\n=== Job Sources Breakdown ===")
        
        if 'source' in self.data.columns:
            source_counts = self.data['source'].value_counts()
            
            for source, count in source_counts.items():
                percentage = (count / self.total_jobs) * 100
                print(f"{source}: {count} jobs ({percentage:.1f}%)")
        else:
            print("X No source information available")
    
    def check_locations(self):
        """
        Check what locations we got jobs from
        """
        print("\n=== Location Breakdown ===")
        
        if 'location' in self.data.columns:
            # Count unique locations
            location_counts = self.data['location'].value_counts().head(10)
            
            print("Top 10 locations:")
            for location, count in location_counts.items():
                if str(location) != 'No Location':
                    percentage = (count / self.total_jobs) * 100
                    print(f"  {location}: {count} jobs ({percentage:.1f}%)")
        else:
            print("X No location information available")
    
    def check_description_quality(self):
        """
        Check if job descriptions are reasonable length
        """
        print("\n=== Description Quality Check ===")
        
        if 'description' in self.data.columns:
            # Calculate description lengths
            desc_lengths = []
            very_short = 0
            
            for desc in self.data['description']:
                if pd.notna(desc) and str(desc) != 'No Description':
                    length = len(str(desc))
                    desc_lengths.append(length)
                    if length < 50:  # Very short descriptions
                        very_short += 1
            
            if desc_lengths:
                avg_length = sum(desc_lengths) / len(desc_lengths)
                print(f"Average description length: {avg_length:.0f} characters")
                print(f"Shortest: {min(desc_lengths)} characters")
                print(f"Longest: {max(desc_lengths)} characters")
                print(f"Very short descriptions (< 50 chars): {very_short}")
                
                if very_short > len(desc_lengths) * 0.3:  # More than 30% are very short
                    print(" Warning: Many descriptions are very short")
                else:
                    print(" Description lengths look reasonable")
            else:
                print(" No valid descriptions found")
        else:
            print("No description field available")
    
    def generate_simple_report(self):
        """
        Create a simple quality report
        """
        if self.data is None:
            print(" No data loaded!")
            return
        
        print(f"\n{'='*60}")
        print(f"DATA QUALITY REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        print(f" SUMMARY:")
        print(f"Total jobs collected: {self.total_jobs}")
        
        # Run all checks
        self.check_required_fields()
        self.check_data_completeness()
        self.check_for_duplicates()
        self.check_job_sources()
        self.check_locations()
        self.check_description_quality()
        
        # Simple overall assessment
        print(f"\n{'='*60}")
        if self.total_jobs >= 20:
            print("GOOD: You have a decent amount of job data!")
        elif self.total_jobs >= 10:
            print("OK: You have some job data, but more would be better.")
        else:
            print("WARNING: Very few jobs collected. Try expanding your search.")
        
        if self.total_jobs > 0:
            print(f"\n NEXT STEPS:")
            print(f"1. If quality looks good, proceed to Stage 2 (Data Preprocessing)")
            print(f"2. If you want more jobs, run the scraper again with different keywords")
            print(f"3. Save this data - you'll use it for the embedding stage!")
        
        print(f"{'='*60}")

def main():
    """
    Main function to check data quality
    """
    print("=== Simple Data Quality Checker ===")
    print("This will check the quality of your collected job data")
    
    # Ask user for the data file
    print("\nWhich file do you want to check?")
    print("Common files: job_postings.csv, api_jobs_*.csv")
    
    filename = input("Enter filename: ").strip()
    
    if not filename:
        # Try common filenames
        import os
        common_files = ['job_postings.csv', 'job_postings.json']
        for file in common_files:
            if os.path.exists(file):
                filename = file
                print(f"Found {filename}")
                break
        
        if not filename:
            print("No data file found. Run the scraper first!")
            return
    
    # Create checker and load data
    checker = SimpleDataChecker()
    
    if checker.load_data(filename):
        # Generate quality report
        checker.generate_simple_report()
    else:
        print("Could not load data file. Make sure the file exists and is valid.")

if __name__ == "__main__":
    main()