#!/usr/bin/env python3
"""
Complete Job Matching System - all stages
Runs the complete pipeline using existing modules from the GitHub repository
"""

import os
import sys
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional
from scipy.spatial.distance import cosine

# Import existing modules from the repository
try:
    from job_scraper import SimpleJobScraper
    from api_scraper import SimpleAPICollector
    from data_validator import SimpleDataChecker
    from embedding_generator import LLMEmbeddingGenerator
    from config import *
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required files are in the same directory!")
    print("Required files: job_scraper.py, api_scraper.py, data_validator.py, embedding_generator.py, config.py")
    sys.exit(1)

class CompleteJobMatchingPipeline:
    """
    Complete job matching pipeline integrating all stages
    """
    
    def __init__(self, location=None, keywords=None, resume_path=None):
        """
        Initialize the complete pipeline
        """
        # Use config values or defaults
        self.location = location or LOCATION
        self.keywords = keywords or KEYWORDS
        self.resume_path = resume_path
        
        # Initialize components
        self.jobs = []
        self.processed_jobs = []
        self.job_embeddings = []
        self.resume_text = ""
        self.resume_embedding = None
        self.similarity_scores = []
        self.top_matches = []
        
        # Initialize embedding generator
        try:
            self.embedding_generator = LLMEmbeddingGenerator()
            print(f"Initialized LLM embedding generator")
        except Exception as e:
            print(f"Warning: Could not initialize embedding generator: {e}")
            self.embedding_generator = None
        
        print("Complete Job Matching Pipeline Initialized")
        print(f"Location: {self.location}")
        print(f"Keywords: {self.keywords}")

    def run_stage1_data_acquisition(self):
        """
        Stage 1: Data Acquisition using existing scrapers
        """
        print("\n" + "="*70)
        print("STAGE 1: DATA ACQUISITION")
        print("="*70)
        
        start_time = time.time()
        
        # Web scraping
        print("Step 1a: Web Scraping...")
        scraper = SimpleJobScraper(location=self.location, keywords=self.keywords)
        scraped_jobs = scraper.scrape_indeed(max_pages=MAX_PAGES_TO_SCRAPE)
        print(f"Scraped {len(scraped_jobs)} jobs from Indeed")
        
        # API collection
        print("\nStep 1b: API Collection...")
        collector = SimpleAPICollector(location=self.location, keywords=self.keywords)
        api_jobs = collector.collect_all_jobs()
        print(f"Collected {len(api_jobs)} jobs from APIs")
        
        # Combine and remove duplicates
        print("\nStep 1c: Combining and deduplicating...")
        all_jobs = scraped_jobs + api_jobs
        self.jobs = self._remove_duplicates(all_jobs)
        
        # Save raw data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_filename = f"raw_jobs_{timestamp}.csv"
        if self.jobs:
            df = pd.DataFrame(self.jobs)
            df.to_csv(raw_filename, index=False)
            print(f"Saved {len(self.jobs)} unique jobs to {raw_filename}")
        
        stage1_time = time.time() - start_time
        print(f"\nStage 1 completed in {stage1_time:.1f} seconds")
        print(f"Total unique jobs collected: {len(self.jobs)}")
        
        return len(self.jobs) > 0

    def run_stage2_data_preprocessing(self):
        """
        Stage 2: Data Preprocessing and Validation
        """
        print("\n" + "="*70)
        print("STAGE 2: DATA PREPROCESSING")
        print("="*70)
        
        start_time = time.time()
        
        if not self.jobs:
            print("Error: No jobs to process. Run Stage 1 first.")
            return False
        
        # Process job data
        print("Step 2a: Processing and cleaning job data...")
        self.processed_jobs = []
        
        for i, job in enumerate(self.jobs):
            processed_job = self._clean_job_data(job)
            if self._is_valid_job(processed_job):
                self.processed_jobs.append(processed_job)
        
        print(f"Processed {len(self.processed_jobs)} valid jobs out of {len(self.jobs)}")
        
        # Process resume
        print("\nStep 2b: Processing resume...")
        if self.resume_path and os.path.exists(self.resume_path):
            self.resume_text = self._load_resume(self.resume_path)
        else:
            print("No resume file provided, using default resume")
            self.resume_text = self._get_default_resume()
        
        self.resume_text = self._clean_text(self.resume_text)
        print(f"Resume processed: {len(self.resume_text)} characters")
        
        # Save processed data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        processed_filename = f"processed_jobs_{timestamp}.csv"
        if self.processed_jobs:
            df = pd.DataFrame(self.processed_jobs)
            df.to_csv(processed_filename, index=False)
            print(f"Saved processed data to {processed_filename}")
        
        # Run data quality check
        print("\nStep 2c: Data quality validation...")
        checker = SimpleDataChecker()
        if checker.load_data(processed_filename):
            checker.generate_simple_report()
        
        stage2_time = time.time() - start_time
        print(f"\nStage 2 completed in {stage2_time:.1f} seconds")
        
        return len(self.processed_jobs) > 0

    def run_stage3_embedding_generation(self):
        """
        Stage 3: Generate embeddings using local LLM
        """
        print("\n" + "="*70)
        print("STAGE 3: EMBEDDING GENERATION")
        print("="*70)
        
        start_time = time.time()
        
        if not self.processed_jobs:
            print("Error: No processed jobs. Run Stage 2 first.")
            return False
        
        if not self.embedding_generator:
            print("Error: Embedding generator not available.")
            return False
        
        # Save processed jobs to temporary CSV for embedding generator
        temp_csv = "temp_jobs_for_embedding.csv"
        df = pd.DataFrame(self.processed_jobs)
        df.to_csv(temp_csv, index=False)
        
        # Load job data into embedding generator
        print("Step 3a: Loading job data into embedding generator...")
        if not self.embedding_generator.load_job_data(temp_csv):
            print("Error: Could not load job data into embedding generator")
            return False
        
        # Generate job embeddings
        print("Step 3b: Generating job embeddings...")
        if not self.embedding_generator.embed_all_jobs():
            print("Error: Could not generate job embeddings")
            return False
        
        # Extract embeddings from the generator
        self.job_embeddings = []
        for item in self.embedding_generator.embeddings:
            self.job_embeddings.append(item['embedding'])
        
        print(f"Generated {len(self.job_embeddings)} job embeddings")
        
        # Generate resume embedding
        print("Step 3c: Generating resume embedding...")
        if not self.embedding_generator.embed_resume(self.resume_text):
            print("Error: Could not generate resume embedding")
            return False
        
        self.resume_embedding = self.embedding_generator.resume_embedding
        print("Resume embedding generated successfully")
        
        # Save embeddings using the generator's method
        self.embedding_generator.save_embeddings()
        
        # Clean up temporary file
        try:
            os.remove(temp_csv)
        except:
            pass
        
        stage3_time = time.time() - start_time
        print(f"\nStage 3 completed in {stage3_time:.1f} seconds")
        print(f"Embedding dimension: {len(self.resume_embedding)}")
        
        return len(self.job_embeddings) == len(self.processed_jobs)

    def run_stage4_similarity_matching(self, top_n=10):
        """
        Stage 4: Calculate similarity and find best matches
        """
        print("\n" + "="*70)
        print("STAGE 4: SIMILARITY CALCULATION AND MATCHING")
        print("="*70)
        
        start_time = time.time()
        
        if not self.job_embeddings or self.resume_embedding is None:
            print("Error: No embeddings available. Run Stage 3 first.")
            return False
        
        print("Step 4a: Calculating cosine similarities...")
        self.similarity_scores = []
        
        resume_emb = np.array(self.resume_embedding)
        
        for i, job_embedding in enumerate(self.job_embeddings):
            try:
                job_emb = np.array(job_embedding)
                
                # Calculate cosine similarity (1 - cosine distance)
                similarity = 1 - cosine(resume_emb, job_emb)
                
                self.similarity_scores.append({
                    'job_index': i,
                    'similarity_score': similarity,
                    'job_data': self.processed_jobs[i]
                })
                
            except Exception as e:
                print(f"Error calculating similarity for job {i}: {e}")
                self.similarity_scores.append({
                    'job_index': i,
                    'similarity_score': 0.0,
                    'job_data': self.processed_jobs[i]
                })
        
        print(f"Calculated similarities for {len(self.similarity_scores)} jobs")
        
        # Sort by similarity score (descending)
        print("Step 4b: Ranking jobs by similarity...")
        self.similarity_scores.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Get top matches
        self.top_matches = self.similarity_scores[:top_n]
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"job_matches_{timestamp}.csv"
        
        match_data = []
        for i, match in enumerate(self.top_matches):
            job = match['job_data']
            match_data.append({
                'rank': i + 1,
                'similarity_score': round(match['similarity_score'], 4),
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'source': job['source'],
                'url': job.get('url', ''),
                'description_preview': job['description'][:200] + "..." if len(job['description']) > 200 else job['description']
            })
        
        df_matches = pd.DataFrame(match_data)
        df_matches.to_csv(results_file, index=False)
        print(f"Saved top {len(self.top_matches)} matches to {results_file}")
        
        stage4_time = time.time() - start_time
        print(f"\nStage 4 completed in {stage4_time:.1f} seconds")
        
        return True

    def display_results(self):
        """
        Display final results
        """
        print("\n" + "="*70)
        print("FINAL RESULTS")
        print("="*70)
        
        if not self.top_matches:
            print("No matches found.")
            return
        
        print(f"\nTop {len(self.top_matches)} Job Matches:")
        print("-" * 70)
        
        for i, match in enumerate(self.top_matches):
            job = match['job_data']
            score = match['similarity_score']
            
            print(f"\n{i+1}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Similarity Score: {score:.4f}")
            print(f"   Source: {job['source']}")
            if job.get('url'):
                print(f"   URL: {job['url']}")
            print(f"   Description: {job['description'][:150]}...")
            print("-" * 50)
        
        # Summary statistics
        scores = [match['similarity_score'] for match in self.similarity_scores]
        print(f"\nSummary Statistics:")
        print(f"  Total jobs analyzed: {len(scores)}")
        print(f"  Average similarity: {np.mean(scores):.4f}")
        print(f"  Best match score: {max(scores):.4f}")
        print(f"  Median similarity: {np.median(scores):.4f}")

    def run_complete_pipeline(self, resume_path=None, top_n=10):
        """
        Run the complete pipeline from Stage 1 to Stage 4
        """
        print("="*80)
        print("COMPLETE JOB MATCHING PIPELINE")
        print("="*80)
        print(f"Target Location: {self.location}")
        print(f"Search Keywords: {self.keywords}")
        print(f"Resume: {resume_path or 'Default resume'}")
        
        if resume_path:
            self.resume_path = resume_path
        
        pipeline_start = time.time()
        
        try:
            # Stage 1: Data Acquisition
            if not self.run_stage1_data_acquisition():
                print("Pipeline failed at Stage 1")
                return False
            
            # Stage 2: Data Preprocessing
            if not self.run_stage2_data_preprocessing():
                print("Pipeline failed at Stage 2")
                return False
            
            # Stage 3: Embedding Generation
            if not self.run_stage3_embedding_generation():
                print("Pipeline failed at Stage 3")
                return False
            
            # Stage 4: Similarity Matching
            if not self.run_stage4_similarity_matching(top_n):
                print("Pipeline failed at Stage 4")
                return False
            
            # Display results
            self.display_results()
            
            total_time = time.time() - pipeline_start
            
            print("\n" + "="*80)
            print("PIPELINE COMPLETED SUCCESSFULLY!")
            print("="*80)
            print(f"Total execution time: {total_time:.1f} seconds")
            print(f"Jobs collected: {len(self.jobs)}")
            print(f"Jobs processed: {len(self.processed_jobs)}")
            print(f"Top matches found: {len(self.top_matches)}")
            
            return True
            
        except KeyboardInterrupt:
            print("\nPipeline interrupted by user")
            return False
        except Exception as e:
            print(f"\nPipeline failed with error: {e}")
            return False

    # Helper methods
    
    def _remove_duplicates(self, jobs):
        """Remove duplicate jobs based on title and company"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            identifier = (
                job.get('title', '').lower().strip(),
                job.get('company', '').lower().strip()
            )
            
            if identifier not in seen and identifier != ('', ''):
                seen.add(identifier)
                unique_jobs.append(job)
        
        print(f"Removed {len(jobs) - len(unique_jobs)} duplicates")
        return unique_jobs

    def _clean_job_data(self, job):
        """Clean job posting data"""
        return {
            'title': self._clean_text(job.get('title', 'Unknown Title')),
            'company': self._clean_text(job.get('company', 'Unknown Company')),
            'location': self._clean_text(job.get('location', 'Unknown Location')),
            'description': self._clean_text(job.get('description', 'No description')),
            'url': job.get('url', ''),
            'source': job.get('source', 'Unknown'),
            'scraped_date': job.get('scraped_date', datetime.now().strftime('%Y-%m-%d'))
        }

    def _clean_text(self, text):
        """Clean text data"""
        if not text:
            return ""
        
        # Remove HTML tags
        import re
        text = re.sub(r'<[^>]+>', ' ', str(text))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def _is_valid_job(self, job):
        """Check if job has minimum required data"""
        return (
            len(job['title'].strip()) > 0 and
            len(job['company'].strip()) > 0 and
            len(job['description'].strip()) >= 50  # Minimum description length
        )

    def _load_resume(self, file_path):
        """Load resume from file"""
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print(f"Note: Only .txt files supported. Using default resume.")
                return self._get_default_resume()
        except Exception as e:
            print(f"Error loading resume: {e}")
            return self._get_default_resume()

    def _get_default_resume(self):
        """Get default resume text"""
        return """
        Software Developer with experience in Python, JavaScript, and web development.
        
        EDUCATION:
        Bachelor of Science in Computer Science
        Saint Louis University - St. Louis
        
        EXPERIENCE:
        Software Developer (2022-2025)
        - Developed web applications using Python and JavaScript
        - Experience with databases and API development
        - Worked with version control and agile methodologies
        
        SKILLS:
        Programming: Python, JavaScript, Java, C++
        Web Development: HTML, CSS, React, Django, Flask
        Databases: PostgreSQL, MongoDB, MySQL
        Tools: Git, Docker, Linux
        
        PROJECTS:
        - Job matching system with AI embeddings
        - Web application with database integration
        - Data analysis and visualization tools
        """


def main():
    """
    Main function to run the complete pipeline
    """
    print("Complete Job Matching System")
    print("Integrating all stages with local LLM embeddings")
    
    # Get user inputs
    location = input(f"Enter job search location (default: {LOCATION}): ").strip()
    if not location:
        location = LOCATION
    
    keywords = input(f"Enter search keywords (default: {KEYWORDS}): ").strip()
    if not keywords:
        keywords = KEYWORDS
    
    resume_path = input("Enter resume file path (.txt) (optional): ").strip()
    if resume_path and not os.path.exists(resume_path):
        print(f"Warning: Resume file not found. Using default resume.")
        resume_path = None
    
    top_n = input("Number of top matches to show (default: 10): ").strip()
    try:
        top_n = int(top_n) if top_n else 10
    except ValueError:
        top_n = 10
    
    # Confirm settings
    print("\nPipeline Configuration:")
    print(f"  Location: {location}")
    print(f"  Keywords: {keywords}")
    print(f"  Resume: {resume_path or 'Default resume'}")
    print(f"  Top matches: {top_n}")
    
    proceed = input("\nProceed with pipeline? (y/n): ").strip().lower()
    if proceed not in ['y', 'yes']:
        print("Exited Pipeline")
        return
    
    # Initialize and run pipeline
    pipeline = CompleteJobMatchingPipeline(
        location=location,
        keywords=keywords,
        resume_path=resume_path
    )
    
    success = pipeline.run_complete_pipeline(resume_path=resume_path, top_n=top_n)
    
    if success:
        print("\nPipeline completed successfully!")
        print("Check the generated CSV files for detailed results.")
    else:
        print("\nPipeline completed with issues.")


if __name__ == "__main__":
    main()