#!/usr/bin/env python3
"""
Stage 3: LLM Embedding Generator
Convert job postings and resume into vector embeddings using local LLM models

Use if you dont want to pay for an API key (which I did)

This script uses sentence-transformers to generate embeddings locally on your computer.
No API keys needed

"""

from sentence_transformers import SentenceTransformer
import pandas as pd
import json
import numpy as np
import time
from datetime import datetime
import os
from typing import List, Dict, Any

class LLMEmbeddingGenerator:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the LLM embedding generator
        """
        print(" Loading local LLM embedding model...")
        print("This might take a minute the first time (downloading model)...")
        
        # Use a good local model - this will download ~25MB first time
        self.model_name = model_name
        try:
            self.model = SentenceTransformer(model_name)
            print(f"Loaded model: {model_name}")
            print(f" Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            print(f" Error loading model: {e}")
            print("Try installing: pip install sentence-transformers")
            raise
        
        self.embeddings = []
        self.job_data = None
        self.resume_embedding = None
    
    def load_job_data(self, filename):
        """
        Load our job data from Stage 1
        """
        try:
            if filename.endswith('.csv'):
                self.job_data = pd.read_csv(filename)
            elif filename.endswith('.json'):
                with open(filename, 'r') as f:
                    jobs_list = json.load(f)
                self.job_data = pd.DataFrame(jobs_list)
            else:
                print("File must be .csv or .json")
                return False
            
            print(f"Loaded {len(self.job_data)} jobs from {filename}")
            return True
            
        except Exception as e:
            print(f"Error loading job data: {e}")
            return False
    
    def prepare_job_text(self, job_row):
        """
        Combine job fields into one text string for embedding
        """
        # Combine title, company, location, and description
        text_parts = []
        
        # Add job title (most important)
        if pd.notna(job_row.get('title')):
            text_parts.append(f"Job Title: {job_row['title']}")
        
        # Add company
        if pd.notna(job_row.get('company')) and job_row['company'] != 'No Company':
            text_parts.append(f"Company: {job_row['company']}")
        
        # Add location
        if pd.notna(job_row.get('location')) and job_row['location'] != 'No Location':
            text_parts.append(f"Location: {job_row['location']}")
        
        # Add description (most content)
        if pd.notna(job_row.get('description')) and job_row['description'] != 'No Description':
            desc = str(job_row['description'])
            # Limit description length for consistency
            if len(desc) > 1000:
                desc = desc[:1000] + "..."
            text_parts.append(f"Description: {desc}")
        
        # Join all parts
        combined_text = " | ".join(text_parts)
        return combined_text
    
    def embed_all_jobs(self):
        """
        Generate embeddings for all job postings using local LLM!
        """
        if self.job_data is None:
            print(" No job data loaded!")
            return False
        
        print(f" Generating LLM embeddings for {len(self.job_data)} jobs...")
        print("This runs on your computer - no internet needed!")
        
        # Prepare all job texts
        job_texts = []
        job_metadata = []
        
        for index, job in self.job_data.iterrows():
            job_text = self.prepare_job_text(job)
            job_texts.append(job_text)
            
            job_metadata.append({
                'job_index': index,
                'title': job.get('title', 'Unknown'),
                'company': job.get('company', 'Unknown'),
                'location': job.get('location', 'Unknown'),
                'text_used': job_text[:200] + "..." if len(job_text) > 200 else job_text
            })
        
        # Generate embeddings in batch (much faster!)
        print("Computing embeddings...")
        try:
            # This is the magic - all embeddings at once, locally!
            embeddings = self.model.encode(job_texts, show_progress_bar=True)
            
            # Combine metadata with embeddings
            for i, embedding in enumerate(embeddings):
                job_metadata[i]['embedding'] = embedding.tolist()  # Convert to list for JSON
            
            self.embeddings = job_metadata
            print(f" Successfully embedded {len(embeddings)} jobs!")
            return True
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return False
    
    def embed_resume(self, resume_text):
        """
        Generate embedding for student's resume using local LLM!
        """
        print("🔄 Generating LLM embedding for resume...")
        
        # Clean up resume text a bit
        if len(resume_text) > 2000:  # Reasonable length
            resume_text = resume_text[:2000] + "..."
        
        try:
            # Generate embedding locally
            embedding = self.model.encode([resume_text])
            self.resume_embedding = embedding[0].tolist()  # Convert to list for JSON
            
            print(" Resume embedding generated successfully!")
            return True
            
        except Exception as e:
            print(f" Error generating resume embedding: {e}")
            return False
    
    def load_resume_from_file(self, filename):
        """
        Load resume text from a file
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                resume_text = f.read()
            
            print(f"Loaded resume from {filename}")
            return self.embed_resume(resume_text)
            
        except Exception as e:
            print(f"Error loading resume file: {e}")
            return False
    
    def save_embeddings(self):
        """
        Save all embeddings to files
        """
        if not self.embeddings:
            print("No embeddings to save!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save job embeddings
        job_embeddings_file = f"job_embeddings_llm_{timestamp}.json"
        
        try:
            with open(job_embeddings_file, 'w') as f:
                json.dump(self.embeddings, f, indent=2)
            print(f"Saved job embeddings to {job_embeddings_file}")
        except Exception as e:
            print(f" Error saving job embeddings: {e}")
        
        # Save resume embedding
        if self.resume_embedding:
            resume_embedding_file = f"resume_embedding_llm_{timestamp}.json"
            try:
                with open(resume_embedding_file, 'w') as f:
                    json.dump({
                        'embedding': self.resume_embedding,
                        'timestamp': timestamp,
                        'model': self.model_name,
                        'dimension': len(self.resume_embedding)
                    }, f, indent=2)
                print(f"Saved resume embedding to {resume_embedding_file}")
            except Exception as e:
                print(f"Error saving resume embedding: {e}")
        
        # Save a summary
        summary_file = f"embedding_summary_llm_{timestamp}.txt"
        try:
            with open(summary_file, 'w') as f:
                f.write(f"LLM Embedding Generation Summary\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Model used: {self.model_name}\n")
                f.write(f"Total job embeddings: {len(self.embeddings)}\n")
                f.write(f"Resume embedded: {'Yes' if self.resume_embedding else 'No'}\n")
                f.write(f"Embedding dimension: {len(self.embeddings[0]['embedding']) if self.embeddings else 'N/A'}\n")
                f.write(f"Cost: $0.00 (Local LLM!)\n")
                f.write(f"Model runs locally - no internet required after download\n")
            print(f"Saved summary to {summary_file}")
        except Exception as e:
            print(f"Error saving summary: {e}")
    
    def show_sample_embeddings(self, num_samples=3):
        """
        Show some sample embeddings info
        """
        if not self.embeddings:
            print("No embeddings to show!")
            return
        
        print(f"\n=== Sample LLM Embeddings (showing first {num_samples}) ===")
        
        for i, item in enumerate(self.embeddings[:num_samples]):
            print(f"\nJob {i+1}:")
            print(f"Title: {item['title']}")
            print(f"Company: {item['company']}")
            print(f"Text used: {item['text_used']}")
            print(f"Embedding dimension: {len(item['embedding'])}")
            print(f"First 5 embedding values: {item['embedding'][:5]}")
            print("-" * 40)
        
        if self.resume_embedding:
            print(f"\nResume Embedding:")
            print(f"Dimension: {len(self.resume_embedding)}")
            print(f"First 5 values: {self.resume_embedding[:5]}")

def create_sample_resume():
    """
    Create a sample resume for testing
    """
    sample_resume = """
John Doe
Computer Science Student
Email: john.doe@siue.edu

EDUCATION
Bachelor of Science in Computer Science
Southern Illinois University - Edwardsville
Expected Graduation: May 2025
GPA: 3.5/4.0

SKILLS
Programming Languages: Python, Java, JavaScript, C++
Web Technologies: HTML, CSS, React, Node.js
Databases: MySQL, PostgreSQL, MongoDB
Tools: Git, Docker, AWS, Linux

EXPERIENCE
Software Development Intern
Tech Inc. - Summer 2024
- Developed web applications using React and Node.js
- Collaborated with team of 5 developers on agile projects

Teaching Assistant - Computer Science
University of Missouri - St. Louis - Fall 2023 to Present
- Assist students with programming assignments in Python and Java
- Grade assignments and provide feedback
- Hold office hours for student questions

PROJECTS
Job Matching System
- Building a system to match resumes with job postings using embeddings
- Using Python, local LLM models, and machine learning techniques

Personal Portfolio Website
- Created responsive website showcasing projects
- Technologies: HTML, CSS, JavaScript, deployed on AWS

CERTIFICATIONS
AWS Cloud Practitioner
Python Programming Certificate
"""
    
    with open('sample_resume.txt', 'w') as f:
        f.write(sample_resume)
    
    print("Created sample_resume.txt for testing")
    return 'sample_resume.txt'

def check_model_availability():
    """
    Check if sentence-transformers is installed and working
    """
    try:
        from sentence_transformers import SentenceTransformer
        print("sentence-transformers is installed")
        return True
    except ImportError:
        print("sentence-transformers not installed")
        print("Install with: pip install sentence-transformers")
        return False

def main():
    """
    Main function to run the LLM embedding generation
    """
    print("=== Stage 3: LLM Embedding Generator ===")
    print("This will convert your job data and resume into vector embeddings")
    print("Uses local LLM models - No API keys")
    
    # Check if required library is installed
    if not check_model_availability():
        print("\nFirst, install the required library:")
        print("pip install sentence-transformers")
        return
    
    # Choose embedding model
    print("\nAvailable LLM models:")
    models = {
        "1": ("all-MiniLM-L6-v2", "Fast, good quality, 384 dimensions"),
        "2": ("all-mpnet-base-v2", "Higher quality, slower, 768 dimensions"),
        "3": ("paraphrase-multilingual-MiniLM-L12-v2", "Multilingual support")
    }
    
    for key, (name, desc) in models.items():
        print(f"  {key}. {name} - {desc}")
    
    choice = input("Choose model (1-3, or press Enter for default): ").strip()
    
    if choice in models:
        model_name = models[choice][0]
    else:
        model_name = "all-MiniLM-L6-v2"  # Default
    
    print(f"Using model: {model_name}")
    
    # Create embedding generator
    try:
        embedder = LLMEmbeddingGenerator(model_name=model_name)
    except Exception as e:
        print(f"Could not load embedding model: {e}")
        return
    
    # Load job data from Stage 1
    print("\nLooking for job data files...")
    job_files = ['final_jobs.csv', 'job_postings.csv', 'scraped_jobs.csv']
    job_file = None
    
    for filename in job_files:
        if os.path.exists(filename):
            job_file = filename
            print(f"Found: {filename}")
            break
    
    if not job_file:
        job_file = input("Enter job data filename: ").strip()
    
    if not embedder.load_job_data(job_file):
        print("Could not load job data!")
        return
    
    # Handle resume
    print("\nNow we need your resume...")
    print("Options:")
    print("1. Load from a text file")
    print("2. Create a sample resume for testing")
    print("3. Enter resume text manually")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        resume_file = input("Enter resume filename: ").strip()
        if not embedder.load_resume_from_file(resume_file):
            return
    elif choice == "2":
        resume_file = create_sample_resume()
        if not embedder.load_resume_from_file(resume_file):
            return
    elif choice == "3":
        print("Enter your resume text (press Ctrl+D when done):")
        resume_lines = []
        try:
            while True:
                line = input()
                resume_lines.append(line)
        except EOFError:
            pass
        resume_text = "\n".join(resume_lines)
        if not embedder.embed_resume(resume_text):
            return
    else:
        print("Invalid choice!")
        return
    
    # Generate embeddings for all jobs
    print(f"\n{'='*50}")
    print("Starting LLM embedding generation...")
    print("This runs entirely on your computer!")
    print(f"{'='*50}")
    
    proceed = input("Proceed? (y/n): ").strip().lower()
    if proceed not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Embed all jobs
    if embedder.embed_all_jobs():
        # Save everything
        embedder.save_embeddings()
        
        # Show sample results
        embedder.show_sample_embeddings()
        
        print(f"\nStage 3 Complete - Local LLM Success!")
        print(f"Generated embeddings for {len(embedder.embeddings)} jobs")
        print(f"Generated embedding for resume")
        print(f"All embeddings saved to files")
        print(f"Total cost: $0.00")
        
        print(f"\nFiles created:")
        print(f"  - job_embeddings_llm_*.json (job embeddings)")
        print(f"  - resume_embedding_llm_*.json (your resume embedding)")
        print(f"  - embedding_summary_llm_*.txt (summary info)")
        
        print(f"\nNext: Stage 4 - Similarity Calculation")
        print(f"Use the generated embedding files to find the most similar jobs!")
        
    else:
        print("Failed to generate embeddings")

if __name__ == "__main__":
    main()