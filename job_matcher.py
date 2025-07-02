#!/usr/bin/env python3
"""
Job Matcher - Stage 4

This script takes embeddings from job postings and a resume, then finds
the most similar jobs using cosine similarity.
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime
import os

# For cosine similarity calculation
from scipy.spatial.distance import cosine

class SimpleJobMatcher:
    def __init__(self):
        self.job_embeddings = []
        self.resume_embedding = None
        self.job_data = []
        self.similarities = []
    
    def load_job_embeddings(self, embeddings_file):
        """
        Load job embeddings from file (JSON or NPY format)
        Expected format: list of embeddings or numpy array
        """
        print(f"Loading job embeddings from {embeddings_file}...")
        
        try:
            if embeddings_file.endswith('.json'):
                with open(embeddings_file, 'r') as f:
                    self.job_embeddings = json.load(f)
                print(f"Loaded {len(self.job_embeddings)} job embeddings from JSON")
            
            elif embeddings_file.endswith('.npy'):
                self.job_embeddings = np.load(embeddings_file)
                print(f"Loaded {len(self.job_embeddings)} job embeddings from NPY")
            
            else:
                print("Embeddings file must be .json or .npy format")
                return False
            
            # Convert to numpy array for easier computation
            self.job_embeddings = np.array(self.job_embeddings)
            return True
            
        except Exception as e:
            print(f"Error loading job embeddings: {e}")
            return False
    
    def load_resume_embedding(self, resume_embedding_file):
        """
        Load resume embedding from file
        """
        print(f"Loading resume embedding from {resume_embedding_file}...")
        
        try:
            if resume_embedding_file.endswith('.json'):
                with open(resume_embedding_file, 'r') as f:
                    self.resume_embedding = json.load(f)
            
            elif resume_embedding_file.endswith('.npy'):
                self.resume_embedding = np.load(resume_embedding_file)
            
            else:
                print("Resume embedding file must be .json or .npy format")
                return False
            
            # Convert to numpy array
            self.resume_embedding = np.array(self.resume_embedding)
            print(f"Loaded resume embedding (dimension: {len(self.resume_embedding)})")
            return True
            
        except Exception as e:
            print(f" Error loading resume embedding: {e}")
            return False
    
    def load_job_data(self, job_data_file):
        """
        Load the original job data (titles, companies, descriptions, etc.)
        This should match the order of the embeddings
        """
        print(f"Loading job data from {job_data_file}...")
        
        try:
            if job_data_file.endswith('.csv'):
                df = pd.read_csv(job_data_file)
                self.job_data = df.to_dict('records')
            
            elif job_data_file.endswith('.json'):
                with open(job_data_file, 'r') as f:
                    self.job_data = json.load(f)
            
            else:
                print(" Job data file must be .csv or .json format")
                return False
            
            print(f"Loaded {len(self.job_data)} job records")
            return True
            
        except Exception as e:
            print(f" Error loading job data: {e}")
            return False
    
    def calculate_similarities(self):
        """
        Calculate cosine similarity between resume and all job postings
        """
        print("Calculating cosine similarities...")
        
        if self.resume_embedding is None:
            print("No resume embedding loaded")
            return False
        
        if len(self.job_embeddings) == 0:
            print("No job embeddings loaded")
            return False
        
        if len(self.job_data) != len(self.job_embeddings):
            print("Number of job embeddings doesn't match number of job records")
            print(f"   Job embeddings: {len(self.job_embeddings)}")
            print(f"   Job records: {len(self.job_data)}")
            return False
        
        self.similarities = []
        
        # Calculate similarity for each job
        for i, job_embedding in enumerate(self.job_embeddings):
            try:
                # Calculate cosine similarity
                # Note: scipy.spatial.distance.cosine gives cosine DISTANCE
                # So similarity = 1 - distance
                cosine_distance = cosine(self.resume_embedding, job_embedding)
                similarity = 1 - cosine_distance
                
                self.similarities.append(similarity)
                
                if i % 10 == 0:  # Progress update every 10 jobs
                    print(f"  Processed {i+1}/{len(self.job_embeddings)} jobs...")
                
            except Exception as e:
                print(f" Error calculating similarity for job {i}: {e}")
                self.similarities.append(0.0)  # Default to 0 similarity
        
        print(f" Calculated similarities for {len(self.similarities)} jobs")
        return True
    
    def get_top_jobs(self, top_n=10):
        """
        Get the top N most similar jobs
        """
        if not self.similarities:
            print(" No similarities calculated yet")
            return []
        
        print(f"Finding top {top_n} most similar jobs...")
        
        # Create list of (similarity, job_index) pairs
        job_similarities = list(enumerate(self.similarities))
        
        # Sort by similarity (descending)
        job_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N
        top_jobs = []
        for i in range(min(top_n, len(job_similarities))):
            job_index, similarity = job_similarities[i]
            
            # Get job data
            job = self.job_data[job_index].copy()
            job['similarity_score'] = similarity
            job['rank'] = i + 1
            
            top_jobs.append(job)
        
        print(f" Found top {len(top_jobs)} jobs")
        return top_jobs
    
    def display_top_jobs(self, top_jobs, show_descriptions=False):
        """
        Display the top jobs in a nice format
        """
        if not top_jobs:
            print("No top jobs to display")
            return
        
        print(f"\n{'='*80}")
        print(f"TOP {len(top_jobs)} MOST SIMILAR JOBS")
        print(f"{'='*80}")
        
        for job in top_jobs:
            print(f"\n RANK {job['rank']}")
            print(f"Similarity Score: {job['similarity_score']:.4f}")
            print(f"Title: {job.get('title', 'No Title')}")
            print(f"Company: {job.get('company', 'No Company')}")
            print(f"Location: {job.get('location', 'No Location')}")
            print(f"Source: {job.get('source', 'Unknown')}")
            
            if show_descriptions and 'description' in job:
                desc = str(job['description'])
                if len(desc) > 200:
                    desc = desc[:200] + "..."
                print(f"Description: {desc}")
            
            if 'url' in job and job['url'] != 'No URL':
                print(f"URL: {job['url']}")
            
            print("-" * 60)
    
    def save_results(self, top_jobs, filename=None):
        """
        Save the top job results to a file
        """
        if not top_jobs:
            print("No results to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"top_jobs_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(top_jobs, f, indent=2)
            print(f"Saved top jobs to {filename}")
            
            # Also save as CSV for easy viewing
            csv_filename = filename.replace('.json', '.csv')
            df = pd.DataFrame(top_jobs)
            df.to_csv(csv_filename, index=False)
            print(f" Also saved as {csv_filename}")
            
        except Exception as e:
            print(f" Error saving results: {e}")
    
    def analyze_results(self, top_jobs):
        """
        Provide some basic analysis of the results
        """
        if not top_jobs:
            print("No results to analyze")
            return
        
        print(f"\n{'='*60}")
        print("RESULTS ANALYSIS")
        print(f"{'='*60}")
        
        # Similarity score statistics
        scores = [job['similarity_score'] for job in top_jobs]
        print(f"Similarity Scores:")
        print(f"  Highest: {max(scores):.4f}")
        print(f"  Lowest: {min(scores):.4f}")
        print(f"  Average: {sum(scores)/len(scores):.4f}")
        
        # Company analysis
        companies = [job.get('company', 'Unknown') for job in top_jobs]
        company_counts = {}
        for company in companies:
            company_counts[company] = company_counts.get(company, 0) + 1
        
        print(f"\nCompanies in top results:")
        for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
            if company != 'Unknown':
                print(f"  {company}: {count} job(s)")
        
        # Location analysis
        locations = [job.get('location', 'Unknown') for job in top_jobs]
        location_counts = {}
        for location in locations:
            location_counts[location] = location_counts.get(location, 0) + 1
        
        print(f"\nLocations in top results:")
        for location, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            if location != 'Unknown':
                print(f"  {location}: {count} job(s)")
        
        # Source analysis
        sources = [job.get('source', 'Unknown') for job in top_jobs]
        source_counts = {}
        for source in sources:
            source_counts[source] = source_counts.get(source, 0) + 1
        
        print(f"\nJob sources in top results:")
        for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
            if source != 'Unknown':
                print(f"  {source}: {count} job(s)")

def main():
    """
    Main function to run the job matching
    """
    print("=== Simple Job Matcher - Stage 4 ===")
    print("This will find the most similar jobs to your resume using embeddings")
    
    # Check if required files exist
    print("\nLooking for required files...")
    
    # Look for job embeddings
    job_embedding_files = []
    for ext in ['*.json', '*.npy']:
        import glob
        files = glob.glob(f"job_embeddings{ext}")
        job_embedding_files.extend(files)
    
    if not job_embedding_files:
        print(" No job embedding files found!")
        print("   Expected files: job_embeddings.json or job_embeddings.npy")
        print("   Make sure you've completed Stage 3 (Embedding Generation)")
        return
    
    # Look for resume embedding
    resume_embedding_files = []
    for ext in ['*.json', '*.npy']:
        files = glob.glob(f"resume_embedding{ext}")
        resume_embedding_files.extend(files)
    
    if not resume_embedding_files:
        print("No resume embedding files found!")
        print("   Expected files: resume_embedding.json or resume_embedding.npy")
        print("   Make sure you've completed Stage 3 (Embedding Generation)")
        return
    
    # Look for job data
    job_data_files = []
    import glob
    for pattern in ['final_jobs_*.csv', 'final_jobs_*.json', 'job_postings.csv']:
        files = glob.glob(pattern)
        job_data_files.extend(files)
    
    if not job_data_files:
        print(" No job data files found!")
        print("   Expected files: final_jobs_*.csv, job_postings.csv, etc.")
        print("   Make sure you've completed Stage 1 (Data Collection)")
        return
    
    # Use the first found files
    job_embeddings_file = job_embedding_files[0]
    resume_embedding_file = resume_embedding_files[0]
    job_data_file = job_data_files[0]
    
    print(f" Using files:")
    print(f"   Job embeddings: {job_embeddings_file}")
    print(f"   Resume embedding: {resume_embedding_file}")
    print(f"   Job data: {job_data_file}")
    
    # Ask user if they want to proceed
    response = input("\nProceed with job matching? (y/n): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Create matcher and load data
    matcher = SimpleJobMatcher()
    
    print(f"\n{'='*60}")
    print("LOADING DATA")
    print(f"{'='*60}")
    
    # Load all required data
    if not matcher.load_job_embeddings(job_embeddings_file):
        return
    
    if not matcher.load_resume_embedding(resume_embedding_file):
        return
    
    if not matcher.load_job_data(job_data_file):
        return
    
    # Calculate similarities
    print(f"\n{'='*60}")
    print("CALCULATING SIMILARITIES")
    print(f"{'='*60}")
    
    if not matcher.calculate_similarities():
        return
    
    # Get top jobs
    print(f"\n{'='*60}")
    print("FINDING TOP MATCHES")
    print(f"{'='*60}")
    
    top_jobs = matcher.get_top_jobs(top_n=10)
    
    if top_jobs:
        # Display results
        matcher.display_top_jobs(top_jobs, show_descriptions=True)
        
        # Analyze results
        matcher.analyze_results(top_jobs)
        
        # Save results
        matcher.save_results(top_jobs)
        
        print(f"\n{'='*60}")
        print("SUCCESS!")
        print(f"{'='*60}")
        print(f"Found {len(top_jobs)} top job matches!")
        print("Results saved to top_jobs_*.json and top_jobs_*.csv")
        print("\nNext steps:")
        print("1. Review the top job matches above")
        print("2. Check if the results make sense for your background")
        print("3. Consider applying to the highest-scoring jobs")
        print("4. Proceed to Stage 5 (Writing Report)")
        
    else:
        print("No top jobs found. Check your embedding files.")

if __name__ == "__main__":
    main()