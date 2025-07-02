#!/usr/bin/env python3
"""
THIS SCRIPT IS ENTIRELY AI GENERATED AND JUST USED FOR TESTING

IMPORTANT: These are just for testing! 
"""

import pandas as pd
import json
import numpy as np
import os
from datetime import datetime

def create_dummy_embeddings():
    """
    Create dummy embeddings for testing the job matcher
    """
    print("=== Creating Dummy Embeddings for Testing ===")
    print("WARNING: These are fake embeddings")
    
    # Look for job data file
    job_data_files = []
    import glob
    for pattern in ['final_jobs_*.csv', 'job_postings.csv', 'scraped_jobs.csv']:
        files = glob.glob(pattern)
        job_data_files.extend(files)
    
    if not job_data_files:
        print("❌ No job data files found!")
        print("   Run Stage 1 first to collect job data")
        return False
    
    job_data_file = job_data_files[0]
    print(f"Using job data from: {job_data_file}")
    
    # Load job data
    try:
        if job_data_file.endswith('.csv'):
            df = pd.read_csv(job_data_file)
            job_data = df.to_dict('records')
        else:
            with open(job_data_file, 'r') as f:
                job_data = json.load(f)
        
        print(f"Loaded {len(job_data)} jobs")
        
    except Exception as e:
        print(f"❌ Error loading job data: {e}")
        return False
    
    # Create dummy embeddings
    embedding_dim = 1536  # Common embedding dimension
    num_jobs = len(job_data)
    
    print(f"Creating {num_jobs} dummy job embeddings (dimension: {embedding_dim})")
    
    # Create random embeddings for jobs
    # Use different random seeds to get variety
    np.random.seed(42)
    job_embeddings = []
    
    for i, job in enumerate(job_data):
        # Create somewhat realistic embedding based on job content
        # This is still random but tries to make similar jobs have similar embeddings
        
        # Use job title and company to create a "base" embedding
        title = str(job.get('title', '')).lower()
        company = str(job.get('company', '')).lower()
        
        # Create base vector
        base_vector = np.random.normal(0, 0.1, embedding_dim)
        
        # Add some patterns based on job type
        if any(word in title for word in ['software', 'developer', 'engineer', 'programmer']):
            base_vector[:100] += np.random.normal(0.2, 0.1, 100)
        
        if any(word in title for word in ['data', 'scientist', 'analyst', 'machine learning']):
            base_vector[100:200] += np.random.normal(0.2, 0.1, 100)
        
        if any(word in title for word in ['manager', 'lead', 'senior', 'director']):
            base_vector[200:300] += np.random.normal(0.2, 0.1, 100)
        
        # Normalize the vector (common practice for embeddings)
        norm = np.linalg.norm(base_vector)
        if norm > 0:
            base_vector = base_vector / norm
        
        job_embeddings.append(base_vector.tolist())
    
    # Create dummy resume embedding
    print("Creating dummy resume embedding")
    np.random.seed(123)  # Different seed for resume
    
    # Make resume embedding somewhat similar to software jobs
    resume_embedding = np.random.normal(0, 0.1, embedding_dim)
    resume_embedding[:100] += np.random.normal(0.3, 0.1, 100)  # Strong software signal
    resume_embedding[300:400] += np.random.normal(0.1, 0.05, 100)  # Some other skills
    
    # Normalize
    norm = np.linalg.norm(resume_embedding)
    if norm > 0:
        resume_embedding = resume_embedding / norm
    
    # Save embeddings
    try:
        # Save job embeddings
        with open('job_embeddings.json', 'w') as f:
            json.dump(job_embeddings, f)
        print("✅ Saved job_embeddings.json")
        
        # Also save as numpy array
        np.save('job_embeddings.npy', np.array(job_embeddings))
        print("✅ Saved job_embeddings.npy")
        
        # Save resume embedding
        with open('resume_embedding.json', 'w') as f:
            json.dump(resume_embedding.tolist(), f)
        print("✅ Saved resume_embedding.json")
        
        # Also save as numpy array
        np.save('resume_embedding.npy', resume_embedding)
        print("✅ Saved resume_embedding.npy")
        
        print(f"\nDummy embeddings created successfully!")
        print(f"You can now test job_matcher.py")
        print(f"\nREMEMBER: These are fake embeddings!")
        print(f"For real job matching, you need to implement Stage 3 (Embedding Generation)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving embeddings: {e}")
        return False

def main():
    """
    Main function
    """
    print("This script creates dummy embeddings for testing Stage 4")
    print("Use this only if you want to test the job matcher before implementing real embeddings")
    
    response = input("\nCreate dummy embeddings for testing? (y/n): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    success = create_dummy_embeddings()
    
    if success:
        print(f"\n{'='*50}")


if __name__ == "__main__":
    main()