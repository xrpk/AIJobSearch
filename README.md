# Job Matching System

A simple project to collect job postings using web scraping and APIs.

## Overview

This project collects job postings from websites, then checks the quality of the data using LLMs.

### Key Features
- **Multi-source data collection** (web scraping)
- **AI-powered matching** using LLMs
- **Automated preprocessing** and quality validation
- **Similarity scoring** with cosine similarity
- **Top job recommendations** with detailed analysis


### Stage 1: Data Acquisition
- **Web Scraping**: Collects jobs from Indeed using BeautifulSoup
- **API Collection**: Fetches jobs from USAJobs, RemoteOK, and RapidAPI
- **Data Validation**: Quality checks and duplicate removal
- **Output**: CSV/JSON files with job postings

### Stage 2: Data Preprocessing
- **Text Cleaning**: Removes HTML, normalize formatting
- **Resume Processing**: Extract and clean resume content
- **Data Standardization**: Consistent field formatting
- **Output**: Preprocessed job data and resume ready for embedding

### Stage 3: Embedding Generation
- **LLM Integration**: Local language models for text analysis
- **Vector Creation**: Convert text to numerical representations using transformers
- **Local Processing**: No API key necessary, runs entirely offline
- **Output**: Embedded vectors for jobs and resume

### Stage 4: Similarity Matching
- **Cosine Similarity**: Calculate job-resume similarity scores
- **Ranking Algorithm**: Sort jobs by relevance
- **Top 10 Selection**: Identify best matches
- **Output**: Ranked list of top job recommendations

## Quick Start

### Prerequisites
- Python 3.8 or newer
- Internet connection (for data collection only)
- GPU recommended for faster LLM process

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/xrpk/AIJobSearch
   cd jobProject
   ```

2. **Set up environment**
   ```bash
   python setup.py
   ```

3. **Install required software**
   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

#### Run Complete Pipeline
```bash
python complete_job_matching_pipeline.py
```
- This will run through each stage in its entirety

#### Alternate Option Run Individual Stages
```bash
# Stage 1: Data Collection
python stage1_complete.py

# Stage 2: Preprocessing (after Stage 1)
python run_all_tests.py

# Stage 3: Generate Embeddings (after Stage 2)
python embedding_generator.py

# Stage 4: Find Matches (after Stage 3)
python create_dummy_embeddings.py
python job_matcher.py
```
- This splits the pipeline into each section, allowing you to test specific areas of the pipeline.


## Configuration

You can edit `config.py` to customize the job search:

```python
# Search parameters
LOCATION = "St. Louis, MO"
KEYWORDS = "software developer computer science python"

# Data collection limits
MAX_PAGES_TO_SCRAPE = 2
MAX_API_JOBS = 10

# Embedding settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Local model
DEVICE = "cuda"  # or "cpu"
BATCH_SIZE = 32

# Matching parameters
TOP_N_JOBS = 10
MIN_SIMILARITY_SCORE = 0.7
```
## Model Setup

### Local LLM Models
This project uses local transformer models for embeddings:
- **No API costs**: Free to run. No unnecessary costs
- **Offline capability**: Works without internet after the first download

#### Models available to use when ran:
1. **sentence-transformers/all-MiniLM-L6-v2**: Fast and efficient
2. **sentence-transformers/all-mpnet-base-v2**: Higher quality but way slower

#### Setup:
```bash
pip install sentence-transformers torch
```

The models will automatically download the first time it is ran (roughly ~70-100MB for MiniLM).

## Data Sources

### Web Scraping
- **Indeed**: Primary job board scraping

### APIs
- **USAJobs**: Government positions (free and no key required)
- **RemoteOK**: Remote opportunities (free no key required)

## Results Analysis

### Matching Performance
The system evaluates matches based on:
- **Similarity scores**: Cosine similarity between resume and job embeddings
- **Keywords**: Common skills and coding languages
- **Location**: location preferences
- **Experience**: Career level matching

### Expected Results
- **High similarity (0.4+)**: Best matches with most overlaps
- **Medium similarity (0.1-0.4)**: Decent match, some learning curve
- **Low similarity (<0.1)**: Potential career Pivots, or large experience gap.

## Potential Future Improvements

### Enhanced Features
- **Model fine-tuning**: Adapt embeddings to specific job domains
- **Multiple model utilization**: Combine different embedding models
- **Advanced Search**: Advanced query understanding
- **Skill ID**: Automatally fnid skills from job descriptions


### Data Sources
- **LinkedIn integration**: Professional network data
- **Company websites**: Direct career page scraping
- **Industry-specific boards(RemoteOK etc.)**: Specialized job platforms


## References

### Documentation
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)




