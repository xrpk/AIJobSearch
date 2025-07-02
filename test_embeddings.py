#!/usr/bin/env python3
"""
Test Script for Local LLM Embeddings
Quick test to make sure setup works before running the full embedding process

"""

def test_installation():
    """
    Test if all required packages are installed
    """
    print("Testing LLM embedding setup...")
    
    required_packages = [
        ('sentence_transformers', 'sentence-transformers'),
        ('torch', 'torch'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas')
    ]
    
    missing_packages = []
    
    for package_name, install_name in required_packages:
        try:
            __import__(package_name)
            print(f"{package_name} - installed")
        except ImportError:
            print(f"{package_name} - MISSING")
            missing_packages.append(install_name)
    
    if missing_packages:
        print(f"\nInstall missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("All required packages installed!")
    return True

def test_model_loading():
    """
    Test loading a small LLM embedding model
    """
    print("\nTesting LLM model loading...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # Try loading the smallest, fastest model
        print("Loading model 'all-MiniLM-L6-v2' (this might take a minute first time)...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("LLM model loaded successfully!")
        print(f"Model info:")
        print(f"  - Name: all-MiniLM-L6-v2")
        print(f"  - Dimensions: {model.get_sentence_embedding_dimension()}")
        print(f"  - Max sequence length: {model.get_max_seq_length()}")
        
        return model
        
    except Exception as e:
        print(f"LLM model loading failed: {e}")
        return None

def test_embedding_generation(model):
    """
    Test generating embeddings with sample text
    """
    print("\nTesting embedding generation...")
    
    try:
        # Test texts
        test_texts = [
            "Software Engineer position at Tech Company in St. Louis, MO",
            "Data Scientist role with Python and machine learning experience",
            "Computer Science student with skills in Java and web development"
        ]
        
        print("Generating embeddings for test texts...")
        embeddings = model.encode(test_texts)
        
        print("Embedding generation successful!")
        print(f"Generated {len(embeddings)} embeddings")
        print(f"Each embedding has {len(embeddings[0])} dimensions")
        print(f"Sample embedding values: {embeddings[0][:5]}")
        
        # Test similarity calculation
        from sklearn.metrics.pairwise import cosine_similarity
        
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        print(f"Similarity between first two texts: {similarity:.4f}")
        
        return True
        
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        return False

def check_system_info():
    """
    Show system information
    """
    print("\nSystem Information:")
    
    import platform
    import psutil
    
    print(f"  - OS: {platform.system()} {platform.release()}")
    print(f"  - Python: {platform.python_version()}")
    print(f"  - CPU cores: {psutil.cpu_count()}")
    print(f"  - RAM: {psutil.virtual_memory().total // (1024**3)} GB")
    
    # Check if GPU is available
    # made with ai help 
    try:
        import torch
        if torch.cuda.is_available():
            print(f"  - GPU: {torch.cuda.get_device_name()}")
            print("  - GPU acceleration available!")
        else:
            print("  - GPU: Not available (will use CPU)")
    except:
        print("  - GPU: Cannot check")

def estimate_performance(num_jobs):
    """
    Estimate how long embedding generation will take
    """
    print(f"\n⏱️ Performance Estimate for {num_jobs} jobs:")
    
    # Rough estimates based on typical performance
    jobs_per_second = 10  # Conservative estimate for CPU
    
    total_seconds = num_jobs / jobs_per_second
    
    if total_seconds < 60:
        print(f"  Estimated time: ~{total_seconds:.0f} seconds")
    else:
        minutes = total_seconds / 60
        print(f"  Estimated time: ~{minutes:.1f} minutes")
    
    print(f"  Processing speed: ~{jobs_per_second} jobs/second")
    print(f"  Note: First run includes model download time")

def main():
    """
    Main test function
    """
    print("=== Local LLM Embeddings Test ===")
    print("This will test your setup for local LLM embedding generation")
    print("No API keys needed, no costs, everything runs locally!")
    
    # Check installations
    if not test_installation():
        print("\nSetup incomplete. Install missing packages first.")
        return
    
    # Check system info
    check_system_info()
    
    # Load model
    model = test_model_loading()
    if not model:
        print("\nLLM model loading failed.")
        return
    
    # Test 4: Generate embeddings
    if not test_embedding_generation(model):
        print("\nEmbedding generation failed.")
        return
    
    # Test 5: Performance estimate
    try:
        num_jobs = int(input("\nHow many jobs do you have in your dataset? "))
        estimate_performance(num_jobs)
    except ValueError:
        print("Skipping performance estimation")
    
    print("\nAll tests passed ====== Your LLM embedding setup is ready")

    
    print("\n💡 Model options:")
    print("  - all-MiniLM-L6-v2: Fast, small, good quality")
    print("  - all-mpnet-base-v2: Higher quality, larger")
    print("  - Choose based on your computer's speed")

if __name__ == "__main__":
    main()