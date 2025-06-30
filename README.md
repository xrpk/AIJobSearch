# Job Matching System - Stage 1: Data Collection

A simple project to collect job postings using web scraping and APIs.

## What This Does

This project collects job postings from websites and APIs, then checks the quality of the data.

## Quick Start

1. **Setup your environment:**
   ```bash
   python setup.py
   ```

2. **Run the complete pipeline:**
   ```bash
   python stage1_complete.py
   ```

3. **Or run individual parts:**
   ```bash
   python job_scraper.py      # Web scraping only
   python api_scraper.py      # API collection only
   python data_validator.py   # Check data quality
   ```

## Files in This Project

- **job_scraper.py** - Scrapes jobs from Indeed
- **api_scraper.py** - Gets jobs from free APIs (USAJobs, RemoteOK)
- **data_validator.py** - Checks if your data is good quality
- **stage1_complete.py** - Runs everything together
- **config.py** - Settings you can change
- **setup.py** - Sets up your computer for the project

## What You Need

- Python 3.8 or newer
- Internet connection
- The Python packages in requirements.txt

Install packages with:
```bash
pip install -r requirements.txt
```

## files produced

After running the scripts, you'll have:

- **scraped_jobs.csv** - Jobs from web scraping
- **api_jobs_*.csv** - Jobs from APIs
- **final_jobs_*.csv** - All jobs combined and cleaned
- A quality report showing how good your data is


## Changing Settings

Edit `config.py` to change:
- Search location (default: St. Louis, MO)
- Keywords (default: computer science, software developer)
- How many pages to scrape
- Wait times between requests

## Troubleshooting

**"No jobs found"**
- Check your internet connection
- Try different keywords in config.py
- Some websites change their structure

**"Import errors"**
- Run `python setup.py` first
- Make sure all files are in the same folder
- Install requirements: `pip install -r requirements.txt`

**"Permission denied" or similar**
- Some websites block scraping
- Try the API collector instead: `python api_scraper.py`


## Stage 2: Data Preprocessing
- clean job descriptions
- remove duplicates
- prepare for embeddings
- clean resume text

### Usage
```bash
python data_preprocessor.py
```


## help things

1. Check the error messages - they usually tell you what's wrong
2. Make sure all .py files are in the same folder
3. Try running `python setup.py` again
4. Look at the examples in each file

## Example Usage

```python
# Simple example of using the scraper
from job_scraper import SimpleJobScraper

scraper = SimpleJobScraper(
    location="Your City, State",
    keywords="your keywords here"
)

jobs = scraper.scrape_indeed(max_pages=2)
scraper.save_to_csv("my_jobs.csv")
```