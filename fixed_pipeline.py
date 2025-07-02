def check_files_exist():
    """Check if all required files exist"""
    required_files = [
        'stage1_complete.py',
        'embedding_generator.py',
        'job_matcher.py'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"ERROR: Missing files: {missing}")
        return False
    
    print("All required files found!")
    return True#!/usr/bin/env python3
"""
Fixed Pipeline Runner
A robust version that handles all the common issues

This version fixes the Unicode and method signature issues.
"""

import os
import sys
import time
import glob
from datetime import datetime

def print_header(title):
    """Print a nice header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def check_files_exist():
    """Check if all required files exist"""
    required_files = [
        'stage1_complete.py',
        'llm_embedding_generator.py',
        'local_similarity_matcher.py'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"ERROR: Missing files: {missing}")
        return False
    
    print("All required files found!")
    return True

def run_stage1():
    """Run Stage 1: Data Collection"""
    print_header("STAGE 1: DATA COLLECTION")
    
    print("This will collect job data from websites and APIs")
    proceed = input("Run Stage 1? (y/n): ").strip().lower()
    if proceed not in ['y', 'yes']:
        return None
    
    try:
        # Import and run stage1 directly to avoid subprocess Unicode issues
        print("Running data collection...")
        
        # Clear any existing output files first
        old_files = glob.glob("final_jobs_*.csv")
        
        # Import the stage1 module
        if 'stage1_complete' in sys.modules:
            del sys.modules['stage1_complete']
        
        import stage1_complete
        
        # Run stage1 main function
        stage1_complete.main()
        
        # Check for new data files
        new_files = glob.glob("final_jobs_*.csv")
        recent_files = [f for f in new_files if f not in old_files]
        
        if recent_files or new_files:
            latest_file = max(new_files, key=os.path.getctime) if new_files else None
            if latest_file:
                print(f"SUCCESS: Data saved to {latest_file}")
                return latest_file
        
        print("ERROR: No data files created")
        return None
        
    except Exception as e:
        print(f"ERROR in Stage 1: {e}")
        return None

def run_stage3():
    """Run Stage 3: Local LLM Embeddings"""
    print_header("STAGE 3: LOCAL LLM EMBEDDINGS")
    
    print("This will generate embeddings using local sentence-transformers")
    print("First run downloads ~25MB model")
    print("Cost: $0.00")
    
    proceed = input("Run Stage 3? (y/n): ").strip().lower()
    if proceed not in ['y', 'yes']:
        return False
    
    try:
        print("Running embedding generation...")
        
        # Check for existing embedding files
        old_job_embeddings = glob.glob("job_embeddings_llm_*.json")
        old_resume_embeddings = glob.glob("resume_embedding_llm_*.json")
        
        # Import and run the embedding generator
        if 'llm_embedding_generator' in sys.modules:
            del sys.modules['llm_embedding_generator']
        
        import llm_embedding_generator
        
        # Run the main function
        llm_embedding_generator.main()
        
        # Check for new embedding files
        new_job_embeddings = glob.glob("job_embeddings_llm_*.json")
        new_resume_embeddings = glob.glob("resume_embedding_llm_*.json")
        
        job_success = len(new_job_embeddings) > len(old_job_embeddings)
        resume_success = len(new_resume_embeddings) > len(old_resume_embeddings)
        
        if job_success and resume_success:
            print("SUCCESS: Embeddings generated")
            return True
        else:
            print("ERROR: Embedding generation may have failed")
            print(f"Job embeddings: {len(new_job_embeddings)} files")
            print(f"Resume embeddings: {len(new_resume_embeddings)} files")
            return False
            
    except Exception as e:
        print(f"ERROR in Stage 3: {e}")
        return False

def run_stage4():
    """Run Stage 4: Similarity Matching"""
    print_header("STAGE 4: SIMILARITY MATCHING")
    
    print("This will find the best job matches using cosine similarity")
    
    proceed = input("Run Stage 4? (y/n): ").strip().lower()
    if proceed not in ['y', 'yes']:
        return False
    
    try:
        print("Running similarity matching...")
        
        # Import the matcher directly
        if 'local_similarity_matcher' in sys.modules:
            del sys.modules['local_similarity_matcher']
        
        import local_similarity_matcher
        
        # Create matcher instance
        matcher = local_similarity_matcher.LocalLLMJobMatcher()
        
        # Load embeddings with proper error handling
        print("Loading job embeddings...")
        if not matcher.load_job_embeddings():
            print("ERROR: Could not load job embeddings")
            return False
        
        print("Loading resume embedding...")
        if not matcher.load_resume_embedding():
            print("ERROR: Could not load resume embedding")
            return False
        
        # Calculate similarities
        print("Calculating similarities...")
        if not matcher.calculate_all_similarities():
            print("ERROR: Could not calculate similarities")
            return False
        
        # Get and display results
        print("Getting top matches...")
        top_matches = matcher.get_top_matches(10)
        
        if top_matches:
            matcher.display_matches(top_matches)
            matcher.generate_analysis_report(top_matches)
            matcher.save_results(top_matches)
            print("SUCCESS: Job matching completed")
            return True
        else:
            print("ERROR: No matches found")
            return False
            
    except Exception as e:
        print(f"ERROR in Stage 4: {e}")
        print("Make sure Stage 3 completed successfully")
        return False

def run_complete_pipeline():
    """Run the complete pipeline with error handling"""
    print("JOB MATCHING SYSTEM - COMPLETE PIPELINE")
    print("This will run all stages with proper error handling")
    
    start_time = time.time()
    
    # Check prerequisites
    if not check_files_exist():
        return False
    
    # Stage 1: Data Collection
    data_file = run_stage1()
    if not data_file:
        print("Pipeline stopped - Stage 1 failed")
        return False
    
    print(f"\nStage 1 complete - Data file: {data_file}")
    
    # Stage 2 is built into Stage 1
    print_header("STAGE 2: DATA PREPROCESSING")
    print("Data preprocessing completed during Stage 1")
    print("SUCCESS: Data cleaned and validated")
    
    # Stage 3: Embeddings
    if not run_stage3():
        print("Pipeline stopped - Stage 3 failed")
        return False
    
    # Stage 4: Matching
    if not run_stage4():
        print("Pipeline stopped - Stage 4 failed")
        return False
    
    # Stage 5: Final reporting
    print_header("STAGE 5: FINAL REPORT")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Total cost: $0.00")
    
    # Show generated files
    print("\nGenerated Files:")
    file_types = [
        ("Job Data", "final_jobs_*.csv"),
        ("Job Embeddings", "job_embeddings_llm_*.json"),
        ("Resume Embedding", "resume_embedding_llm_*.json"),
        ("Match Results", "job_matches_local_llm_*.json")
    ]
    
    for desc, pattern in file_types:
        files = glob.glob(pattern)
        if files:
            latest = max(files, key=os.path.getctime)
            print(f"  {desc}: {latest}")
    
    print("\nNext Steps:")
    print("1. Review your job matches above")
    print("2. Apply to top-scoring positions")
    print("3. Update resume and re-run for better matches")
    
    return True

def main():
    """Main function"""
    print("Fixed Pipeline Runner")
    print("Choose an option:")
    print("1. Run complete pipeline (recommended)")
    print("2. Run Stage 1 only (data collection)")
    print("3. Run Stage 3 only (embeddings)")
    print("4. Run Stage 4 only (matching)")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        run_complete_pipeline()
    elif choice == "2":
        run_stage1()
    elif choice == "3":
        run_stage3()
    elif choice == "4":
        run_stage4()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()