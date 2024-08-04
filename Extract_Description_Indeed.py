import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# Set up the WebDriver service and options
service = Service() 
options = webdriver.ChromeOptions()
options.add_argument("--incognito")


def fetch_description(url):
    """Fetch the job description from the given URL."""
    driver = None
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        # Wait for the job description element to be present
        wait = WebDriverWait(driver, 15)
        try:
            description_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'jobsearch-JobComponent-description'))
            )
            # Get the text, clean it up, and return it
            description = description_element.text.strip()
            return re.sub(r'\s+', ' ', description)
        except Exception as e:
            print(f"Description element not found for {url}. Page source: {driver.page_source[:5000]}")
            return None
    except Exception as e:
        print(f"Error fetching description from {url}: {e}")
        return None
    finally:
        if driver:
            driver.quit()

# Read input CSV file
input_csv_path = 'scraped_job_file.csv'  # Path to your input CSV file
df = pd.read_csv(input_csv_path)

# List to store job descriptions
descriptions = []

# Process each job URL in the DataFrame
for index, row in df.iterrows():
    job_id = row['Job ID']
    url = row['URL']
    description = fetch_description(url)
    descriptions.append({'Job ID': job_id, 'Description': description})
    time.sleep(1)  # Optional: Add delay between requests

# Convert descriptions list to DataFrame
descriptions_df = pd.DataFrame(descriptions)

# Merge descriptions with the original DataFrame
merged_df = pd.merge(df, descriptions_df, on='Job ID', how='left')

# Save the updated DataFrame back to CSV
merged_df.to_csv(input_csv_path, index=False)

print(f"Job descriptions have been updated in {input_csv_path}")
