# Glassdoor Scraper
I designed a scraping 🕸️ tool to extract job posting data from Glassdoor. This scraping tool will return job title, company name, job id, location, salary, language and skills and many more.

*It was easier to extract Glassdoor data compared to Indeed because job postings in Glassdoor are organized, properly labelled and glassdoor also provides estimated salary (if not present).*

**Thank you Glassdoor**

<br>

## Step 1: Install dependencies

Install required dependencies in your project folder.

```
pip install -r requirements.txt
```
<br>

## Step 2: Run Glassdoor_Scraper.py

Make sure you have Chrome ⬇️ latest version installed in your system. This step creates `scraped_glassdoor_job_file.csv` with all columns. *You can check the sample output in this repository itself, I extracted for Data Analyst Position in Canada.*
<br>



### Further Work:

Currently, only one web address can be processed during each run. Create a list of different addresses, and pass the index value; the tool should fetch each url one by one, and scrap accordingly, and create a final output or multiple outputs.


#### Follow my data-analyst journey: [Portfolio_Link](https://www.amanbhattarai.com)
