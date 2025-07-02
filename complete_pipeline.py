#!/usr/bin/env python3
"""
Complete Job Matching Pipeline - Local LLM Version
Stages 1-5: End-to-end job matching system using local LLM embeddings

"""

import os
import sys
import time
from datetime import datetime
import subprocess

def print_stage_header(stage_num, title):
    """Print a nice header for each stage"""
    print(f"\n{'='*70}")
    print(f"STAGE {stage_num}: {title}")
    print(f"{'='*70}")

def check_requirements():
    """Check if all required files and packages are available"""
    print("Checking system requirements...")
    
    required_files = [
        'job_scraper.py',
        'api_scraper.py', 
        'data_validator.py',
        'stage1_complete.py',
        'embedding_generator.py',  # Local LLM version
        'job_matcher.py'   # Local similarity matcher
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing required files: {missing_files}")
        return False
    
    # Check required packages
    required_packages = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('pandas', 'pandas'),
        ('sentence-transformers', 'sentence_transformers'),
        ('scipy', 'scipy'),
        ('numpy', 'numpy')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"Missing required packages: {missing_packages}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("✓ All requirements satisfied")
    return True

def run_stage1_data_collection():
    """Run Stage 1: Data Collection"""
    print_stage_header(1, "DATA COLLECTION")
    
    try:
        # Run the data collection pipeline
        print("Running data collection pipeline...")
        result = subprocess.run([sys.executable, 'stage1_complete.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Check if we got data files
            import glob
            job_files = glob.glob("final_jobs_*.csv")
            
            if job_files:
                latest_file = max(job_files, key=os.path.getctime)
                print(f"✓ Stage 1 complete. Data saved to: {latest_file}")
                return latest_file
            else:
                print("✗ Stage 1 failed - no data files generated")
                return None
        else:
            print(f"✗ Stage 1 failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"✗ Stage 1 failed: {e}")
        return None

def run_stage2_preprocessing(data_file):
    """Run Stage 2: Data Preprocessing"""
    print_stage_header(2, "DATA PREPROCESSING & VALIDATION")
    
    print("Data preprocessing was completed during collection stage")
    
    # Run data validation
    try:
        from data_validator import SimpleDataChecker
        
        checker = SimpleDataChecker()
        if checker.load_data(data_file):
            print("Running data quality check...")
            checker.generate_simple_report()
            print("✓ Stage 2 complete - data preprocessing and validation done")
            return True
        else:
            print("✗ Stage 2 failed - could not validate data")
            return False
            
    except Exception as e:
        print(f"✗ Stage 2 failed: {e}")
        return False

def run_stage3_local_embeddings(data_file):
    """Run Stage 3: Local LLM Embedding Generation"""
    print_stage_header(3, "LOCAL LLM EMBEDDING GENERATION")
    
    print("This stage will generate embeddings using a local LLM model")
    print("First run downloads ~25MB model, then everything runs offline!")
    print("Cost: $0.00")
    
    proceed = input("\nProceed with local embedding generation? (y/n): ").strip().lower()
    if proceed not in ['y', 'yes']:
        print("Stage 3 skipped by user")
        return False
    
    try:
        # Import and run the local LLM embedding generator
        print("Running local LLM embedding generation...")
        
        # We'll simulate the embedding process for the pipeline
        # In practice, you'd run the embedding_generator.py script
        from embedding_generator import LLMEmbeddingGenerator, create_sample_resume
        
        # Create embedder with default model
        embedder = LLMEmbeddingGenerator()
        
        # Load job data
        if not embedder.load_job_data(data_file):
            print("✗ Stage 3 failed - could not load job data")
            return False
        
        # Handle resume - create sample for pipeline demo
        print("Creating sample resume for pipeline demo...")
        resume_file = create_sample_resume()
        
        if not embedder.load_resume_from_file(resume_file):
            print("✗ Stage 3 failed - could not load resume")
            return False
        
        # Generate embeddings
        print("Generating local LLM embeddings...")
        if embedder.embed_all_jobs():
            # Save embeddings
            embedder.save_embeddings()
            print("✓ Stage 3 complete - embeddings generated and saved")
            return True
        else:
            print("✗ Stage 3 failed - could not generate embeddings")
            return False
            
    except Exception as e:
        print(f"✗ Stage 3 failed: {e}")
        return False

def run_stage4_local_matching():
    """Run Stage 4: Local Similarity Matching"""
    print_stage_header(4, "LOCAL SIMILARITY MATCHING")
    
    try:
        from job_matcher import SimpleJobMatcher
        
        # Create matcher
        matcher = SimpleJobMatcher()
        
        # Load embeddings
        print("Loading job embeddings...")
        if not matcher.load_job_embeddings():
            print("✗ Stage 4 failed - could not load job embeddings")
            return None
        
        print("Loading resume embedding...")
        if not matcher.load_resume_embedding():
            print("✗ Stage 4 failed - could not load resume embedding")
            return None
        
        # Calculate similarities
        print("Calculating job similarities...")
        if not matcher.calculate_all_similarities():
            print("✗ Stage 4 failed - could not calculate similarities")
            return None
        
        # Get top matches
        top_matches = matcher.get_top_matches(10)
        
        if not top_matches:
            print("✗ Stage 4 failed - no matches found")
            return None
        
        print(f"✓ Stage 4 complete - found {len(top_matches)} job matches")
        return matcher, top_matches
        
    except Exception as e:
        print(f"✗ Stage 4 failed: {e}")
        return None

def run_stage5_analysis_and_reporting(matcher, top_matches):
    """Run Stage 5: Results Analysis and Reporting"""
    print_stage_header(5, "RESULTS ANALYSIS & REPORTING")
    
    try:
        # Display results
        print("Displaying top job matches...")
        matcher.display_matches(top_matches)
        
        # Generate detailed analysis
        matcher.generate_analysis_report(top_matches)
        
        # Save results
        results_file = matcher.save_results(top_matches)
        
        # Generate final summary report
        print(f"\n{'='*60}")
        print("FINAL PROJECT SUMMARY")
        print(f"{'='*60}")
        
        scores = [match['similarity'] for match in top_matches]
        
        print(f"Project Implementation: Complete")
        print(f"Total stages completed: 5/5")
        print(f"Embedding method: Local LLM (sentence-transformers)")
        print(f"Total cost: $0.00")
        print(f"Jobs processed: {len(matcher.similarities)}")
        print(f"Top matches found: {len(top_matches)}")
        print(f"Best match score: {max(scores):.4f}")
        print(f"Average match score: {sum(scores)/len(scores):.4f}")
        
        # Technical achievements
        print(f"\nTechnical Achievements:")
        print(f"✓ Web scraping with ethical rate limiting")
        print(f"✓ API integration with multiple job sources")
        print(f"✓ Local LLM embedding generation")
        print(f"✓ Cosine similarity calculation")
        print(f"✓ Comprehensive data validation")
        print(f"✓ Results analysis and reporting")
        
        # Files created
        print(f"\nFiles Generated:")
        import glob
        
        job_files = glob.glob("final_jobs_*.csv")
        embedding_files = glob.glob("job_embeddings_llm_*.json")
        resume_files = glob.glob("resume_embedding_llm_*.json")
        result_files = glob.glob("job_matches_local_llm_*.json")
        
        if job_files:
            print(f"  📊 Job Data: {job_files[-1]}")
        if embedding_files:
            print(f"  🧠 Job Embeddings: {embedding_files[-1]}")
        if resume_files:
            print(f"  📝 Resume Embedding: {resume_files[-1]}")
        if result_files:
            print(f"  🎯 Match Results: {result_files[-1]}")
        
        print(f"✓ Stage 5 complete - comprehensive analysis generated")
        return True
        
    except Exception as e:
        print(f"✗ Stage 5 failed: {e}")
        return False

def main():
    """
    Main function to run the complete local LLM pipeline
    """
    print("COMPLETE JOB MATCHING SYSTEM - LOCAL LLM VERSION")
    print("This pipeline runs entirely on your computer - no API costs!")
    
    print("\nSystem Overview:")
    print("Stage 1: Data Collection (web scraping + APIs)")
    print("Stage 2: Data Preprocessing (cleaning + validation)")
    print("Stage 3: Local LLM Embeddings (sentence-transformers)")
    print("Stage 4: Similarity Matching (cosine similarity)")
    print("Stage 5: Analysis & Reporting (comprehensive results)")
    
    print(f"\nBenefits of Local LLM Approach:")
    print(f"* $0.00 cost - no API fees")
    print(f"* Runs offline after initial model download")
    print(f"* Privacy - your data never leaves your computer")
    print(f"* No API key management required")
    print(f"* Reproducible results")
    
    # Ask user if they want to proceed
    response = input("\nRun complete local pipeline? (y/n): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Pipeline cancelled.")
        return
    
    # Check requirements
    if not check_requirements():
        print("Please fix requirements before running pipeline.")
        print("Missing sentence-transformers? Install with:")
        print("pip install sentence-transformers")
        return
    
    start_time = time.time()
    
    try:
        # Stage 1: Data Collection
        data_file = run_stage1_data_collection()
        if not data_file:
            print("Pipeline stopped - Stage 1 failed")
            return
        
        # Stage 2: Data Preprocessing  
        if not run_stage2_preprocessing(data_file):
            print("Pipeline stopped - Stage 2 failed")
            return
        
        # Stage 3: Local LLM Embedding Generation
        if not run_stage3_local_embeddings(data_file):
            print("Pipeline stopped - Stage 3 failed")
            return
        
        # Stage 4: Local Similarity Matching
        result = run_stage4_local_matching()
        if result is None:
            print("Pipeline stopped - Stage 4 failed")
            return
        
        matcher, top_matches = result
        
        # Stage 5: Analysis and Reporting
        if not run_stage5_analysis_and_reporting(matcher, top_matches):
            print("Pipeline stopped - Stage 5 failed")
            return
        
        # Final success summary
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n{'='*70}")
        print("PIPELINE COMPLETE - LOCAL LLM SUCCESS!")
        print(f"{'='*70}")
        print(f"Total execution time: {total_time/60:.1f} minutes")
        print(f"Total cost: $0.00")
        print(f"Jobs processed: {len(matcher.similarities)}")
        print(f"Best matches found: {len(top_matches)}")
        
        print(f"\nPROJECT ACHIEVEMENTS:")
        print(f"* Successfully implemented all 5 stages")
        print(f"* Used modern NLP techniques (sentence transformers)")
        print(f"* Demonstrated web scraping and API integration")
        print(f"* Applied vector similarity search")
        print(f"* Generated comprehensive analysis and reporting")
        print(f"* Cost-effective solution using local resources")
        
        print(f"\nNEXT STEPS:")
        print(f"1. Review your top job matches above")
        print(f"2. Customize your resume based on match analysis")
        print(f"3. Apply to jobs with highest similarity scores")
        print(f"4. Re-run pipeline with updated resume for better matches")
        print(f"5. Expand to additional job sources for more data")
        
        print(f"\nFOR YOUR REPORT:")
        print(f"- Embedding model used: sentence-transformers/all-MiniLM-L6-v2")
        print(f"- Similarity metric: Cosine similarity")
        print(f"- Data sources: Indeed (scraping) + USAJobs + RemoteOK (APIs)")
        print(f"- Processing pipeline: 5 complete stages")
        print(f"- Cost analysis: $0.00 using local compute resources")
        
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user")
    except Exception as e:
        print(f"\nPipeline failed with error: {e}")
        print("Check the error messages above for details")

if __name__ == "__main__":
    main()