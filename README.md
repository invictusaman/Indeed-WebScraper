# Indeed Scraper
I created a webscraper 🕸️ tool to fetch indeed data. It will return job title, company name, job id, url of the job, salary(if present) and whole description of respective job.

## Step 1: Install dependencies

Install required dependencies in your project folder.

```
pip install -r requirements.txt
```

## Step 2: Run Indeed_Scraper.py

Make sure you have Chrome ⬇️ latest version installed in your system. This step creates `scraped_job_file.csv`, however, you won't have job descriptions. 

## Step 3: Run Extract_Description_Indeed.py

**Recommended: Clean your `scraped_job_file.csv` for duplicate values, before running this code.**

This step extracts `job_description` and assign them to the respective rows. It will take good amount of time, go grab a coffee ☕. O/P is updated `scraped_job_file.csv` with merged job description.

*I did not implement multi threading 🧵 (which would have otherwise saved you a lot of time), because of time and limited knowledge. Feel free to fork this repo and implement. Good luck. 🤓*

### Further Work:

Implement a pretrained NER model and extract information such as programming languages included, type of work(remote, hybrid, in-person), salaries from description column. Or, you can use simple logic to match respective words.

#### Follow my data-analyst journey: [Portfolio_Link](https://www.amanbhattarai.com)

