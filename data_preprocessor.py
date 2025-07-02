#!/usr/bin/env python3
"""
Stage 2: Data Preprocessing 
cleans up the stuff from stage 1
"""

import pandas as pd
import re
import json
from datetime import datetime

class SimpleJobCleaner:
    def __init__(self):
        self.jobs_data = None
        self.original_count = 0
        self.final_count = 0
    
    def load_jobs(self, filename):
        """Load job data from CSV or JSON file"""
        try:
            if filename.endswith('.csv'):
                self.jobs_data = pd.read_csv(filename)
            elif filename.endswith('.json'):
                with open(filename, 'r') as f:
                    jobs_list = json.load(f)
                self.jobs_data = pd.DataFrame(jobs_list)
            else:
                print("Error: File must be .csv or .json")
                return False
            
            self.original_count = len(self.jobs_data)
            print(f"Loaded {self.original_count} jobs from {filename}")
            return True
            
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def remove_html_tags(self, text):
        """Remove HTML tags from text (like <p>, <br>, etc.)"""
        if pd.isna(text):
            return ""
        
        # Remove HTML tags
        clean_text = re.sub(r'<.*?>', '', str(text))
        
        # Fix common HTML entities
        clean_text = clean_text.replace('&amp;', '&')
        clean_text = clean_text.replace('&lt;', '<')
        clean_text = clean_text.replace('&gt;', '>')
        clean_text = clean_text.replace('&quot;', '"')
        
        return clean_text
    
    def clean_whitespace(self, text):
        """Clean up extra spaces and weird characters"""
        if pd.isna(text):
            return ""
        
        text = str(text)
        
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing spaces
        text = text.strip()
        
        return text
    
    def fix_locations(self, location):
        """Standardize location names"""
        if pd.isna(location):
            return "Unknown"
        
        location = str(location).strip()
        
        # Fix common variations
        if 'St. Louis' in location or 'St Louis' in location:
            location = location.replace('St. Louis', 'Saint Louis')
            location = location.replace('St Louis', 'Saint Louis')
        
        if 'KC' in location:
            location = location.replace('KC', 'Kansas City')
        
        return location
    
    def clean_job_title(self, title):
        """Clean up job titles"""
        if pd.isna(title):
            return "Unknown Position"
        
        title = str(title).strip()
        
        # Remove common prefixes
        if title.startswith('Job:'):
            title = title[4:].strip()
        if title.startswith('Position:'):
            title = title[9:].strip()
        if title.startswith('Hiring:'):
            title = title[7:].strip()
        
        return title
    
    def clean_description(self, description):
        """Clean job descriptions"""
        if pd.isna(description):
            return ""
        
        description = str(description)
        
        # Handle placeholder text
        if description in ['No Description', 'N/A', 'NA', '']:
            return ""
        
        # Remove HTML
        description = self.remove_html_tags(description)
        
        # Clean whitespace
        description = self.clean_whitespace(description)
        
        # Remove common boilerplate text
        boilerplate = [
            'equal opportunity employer',
            'apply now',
            'click here to apply',
            'send resume to'
        ]
        
        for phrase in boilerplate:
            description = re.sub(phrase, '', description, flags=re.IGNORECASE)
        
        description = self.clean_whitespace(description)
        
        return description
    
    def remove_duplicates(self):
        """Remove duplicate job postings"""
        print("Removing duplicates...")
        
        before_count = len(self.jobs_data)
        
        # Create a key to check for duplicates
        self.jobs_data['temp_key'] = (
            self.jobs_data['title'].str.lower() + '|' + 
            self.jobs_data['company'].str.lower()
        )
        
        # Remove duplicates
        self.jobs_data = self.jobs_data.drop_duplicates(subset=['temp_key'])
        
        # Remove the temporary column
        self.jobs_data = self.jobs_data.drop('temp_key', axis=1)
        
        after_count = len(self.jobs_data)
        removed = before_count - after_count
        
        print(f"Removed {removed} duplicate jobs")
    
    def remove_bad_jobs(self):
        """Remove jobs that don't have enough information"""
        print("Removing incomplete jobs...")
        
        before_count = len(self.jobs_data)
        
        # Remove jobs without title or company
        self.jobs_data = self.jobs_data[
            (self.jobs_data['title'].notna()) & 
            (self.jobs_data['title'] != '') &
            (self.jobs_data['company'].notna()) & 
            (self.jobs_data['company'] != '')
        ]
        
        # Remove jobs with very short descriptions
        self.jobs_data = self.jobs_data[
            (self.jobs_data['description'].str.len() >= 20) | 
            (self.jobs_data['description'].isna())
        ]
        
        after_count = len(self.jobs_data)
        removed = before_count - after_count
        
        print(f"Removed {removed} incomplete jobs")
    
    def create_clean_text(self):
        """Create a clean text field for embeddings"""
        print("Creating text for embeddings...")
        
        clean_texts = []
        
        for _, job in self.jobs_data.iterrows():
            # Combine the important parts
            parts = []
            
            if pd.notna(job['title']):
                parts.append(f"Title: {job['title']}")
            
            if pd.notna(job['company']):
                parts.append(f"Company: {job['company']}")
            
            if pd.notna(job['location']):
                parts.append(f"Location: {job['location']}")
            
            if pd.notna(job['description']) and job['description']:
                parts.append(f"Description: {job['description']}")
            
            # Join everything together
            clean_text = " | ".join(parts)
            clean_texts.append(clean_text)
        
        self.jobs_data['clean_text'] = clean_texts
    
    def clean_all_jobs(self):
        """Clean all the job data"""
        if self.jobs_data is None:
            print("No data loaded!")
            return None
        
        print("\n=== Starting Job Cleaning ===")
        print(f"Starting with {len(self.jobs_data)} jobs")
        
        # Clean each field
        print("\n1. Cleaning titles...")
        self.jobs_data['title'] = self.jobs_data['title'].apply(self.clean_job_title)
        
        print("2. Fixing locations...")
        self.jobs_data['location'] = self.jobs_data['location'].apply(self.fix_locations)
        
        print("3. Cleaning company names...")
        self.jobs_data['company'] = self.jobs_data['company'].apply(self.clean_whitespace)
        
        print("4. Cleaning descriptions...")
        self.jobs_data['description'] = self.jobs_data['description'].apply(self.clean_description)
        
        # Remove bad data
        print("\n5. Removing duplicates and bad jobs...")
        self.remove_duplicates()
        self.remove_bad_jobs()
        
        # Create final text
        print("\n6. Creating clean text for embeddings...")
        self.create_clean_text()
        
        self.final_count = len(self.jobs_data)
        
        print(f"\n=== Cleaning Complete ===")
        print(f"Final job count: {self.final_count}")
        print(f"Removed: {self.original_count - self.final_count} jobs")
        
        return self.jobs_data
    
    def save_clean_data(self, filename=None):
        """Save the cleaned data"""
        if self.jobs_data is None or len(self.jobs_data) == 0:
            print("No data to save!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if filename is None:
            filename = f"clean_jobs_{timestamp}.csv"
        
        try:
            self.jobs_data.to_csv(filename, index=False)
            print(f"Saved cleaned data to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving data: {e}")
            return None
    
    def show_samples(self, num=3):
        """Show some sample cleaned jobs"""
        if self.jobs_data is None or len(self.jobs_data) == 0:
            print("No data to show!")
            return
        
        print(f"\n=== Sample Cleaned Jobs ===")
        
        for i in range(min(num, len(self.jobs_data))):
            job = self.jobs_data.iloc[i]
            print(f"\nJob {i+1}:")
            print(f"Title: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Description: {job['description'][:100]}...")
            print(f"Clean Text: {job['clean_text'][:100]}...")
            print("-" * 50)


class ResumeTextCleaner:
    """Simple resume text cleaner"""
    
    def __init__(self):
        self.resume_text = ""
        self.clean_text = ""
    
    def load_resume(self, filename=None, text=None):
        """Load resume from file or text"""
        try:
            if filename:
                with open(filename, 'r') as f:
                    self.resume_text = f.read()
                print(f"Loaded resume from {filename}")
            elif text:
                self.resume_text = text
                print("Loaded resume from text input")
            else:
                print("Need either filename or text")
                return False
            
            return True
        except Exception as e:
            print(f"Error loading resume: {e}")
            return False
    
    def clean_resume(self):
        """Clean the resume text"""
        if not self.resume_text:
            print("No resume text to clean")
            return ""
        
        print("Cleaning resume text...")
        
        text = self.resume_text
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove weird characters
        text = re.sub(r'[^\x20-\x7E\n]', '', text)
        
        self.clean_text = text
        print(f"Resume cleaned: {len(self.clean_text)} characters")
        
        return self.clean_text
    
    def save_clean_resume(self, filename=None):
        """Save cleaned resume"""
        if not self.clean_text:
            print("No cleaned resume to save")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"clean_resume_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(self.clean_text)
            print(f"Saved clean resume to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving resume: {e}")
            return None


def main():
    """Main function to run the cleaning"""
    print("=== Stage 2: Data Preprocessing ===")
    print("This will clean up your job data from Stage 1")
    
    # Get the job data file
    print("\nWhat's your job data file from Stage 1?")
    print("(Try: final_jobs_*.csv, scraped_jobs.csv, or similar)")
    
    filename = input("Filename: ").strip()
    
    if not filename:
        # Look for common files
        import os
        files = [f for f in os.listdir('.') if f.endswith('.csv') and 'job' in f.lower()]
        if files:
            filename = files[0]  # Use first one found
            print(f"Using: {filename}")
        else:
            print("No job files found. Run Stage 1 first!")
            return
    
    # Clean the job data
    cleaner = SimpleJobCleaner()
    
    if not cleaner.load_jobs(filename):
        return
    
    cleaned_data = cleaner.clean_all_jobs()
    
    if cleaned_data is None or len(cleaned_data) == 0:
        print("No jobs left after cleaning!")
        return
    
    # Show some examples
    cleaner.show_samples()
    
    # Save the cleaned data
    clean_filename = cleaner.save_clean_data()
    
    # Ask about resume
    print("\nDo you want to clean your resume text too? (y/n)")
    if input().lower().startswith('y'):
        resume_cleaner = ResumeTextCleaner()
        
        print("\nChoose:")
        print("1. Type resume text")
        print("2. Load from file")
        
        choice = input("Choice (1 or 2): ").strip()
        
        if choice == '1':
            print("Paste your resume text here, then press Enter twice:")
            lines = []
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            
            resume_text = "\n".join(lines[:-1])  # Remove the last empty line
            
            if resume_cleaner.load_resume(text=resume_text):
                resume_cleaner.clean_resume()
                resume_cleaner.save_clean_resume()
        
        elif choice == '2':
            resume_file = input("Resume filename: ").strip()
            if resume_cleaner.load_resume(filename=resume_file):
                resume_cleaner.clean_resume()
                resume_cleaner.save_clean_resume()
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Original jobs: {cleaner.original_count}")
    print(f"Clean jobs: {cleaner.final_count}")
    print(f"Saved to: {clean_filename}")
    
    print(f"\nNext: Use {clean_filename} for Stage 3 (Embeddings)")
    print("You'll need an API key (OpenAI or Google) for Stage 3")


if __name__ == "__main__":
    main()