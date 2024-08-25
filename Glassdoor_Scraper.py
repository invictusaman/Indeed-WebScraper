# Program to Scrape Job Information from GlassDoor
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# List to hold job data
jobs_list = []

# Define the URL
# Search on Glassdoor for the job position, and it will generate a unique URL
url = "https://www.glassdoor.ca/Job/canada-data-analyst-jobs-SRCH_IL.0,6_IN3_KO7,19.htm"

# Set up the WebDriver service and options
service = Service()
options = webdriver.ChromeOptions()
# Uncomment to run Chrome in headless mode
# options.add_argument("--headless")
options.add_argument("--incognito")
driver = webdriver.Chrome(service=service, options=options)

# Glassdoor pops up Login modal after visiting 2 or 3 pages
# Also, it occurs only one time
# Close if present
def close_modal_if_present():
    try:
        # Check if modal is present and close it
        modal_close_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.CloseButton"))
        )
        # Scroll into view and click close button
        driver.execute_script("arguments[0].scrollIntoView(true);", modal_close_button)
        modal_close_button.click()
        time.sleep(2)  # Wait for the modal to close
    except Exception as e:
        print(f"Modal not present or error closing modal: {e}")

try:
    driver.get(url)

    # Wait for the job listings to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.JobsList_jobsList__lqjTr"))
    )

    while True:
        # Extract page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the container with the job listings
        all_jobs_container = soup.find("ul", class_="JobsList_jobsList__lqjTr")

        if all_jobs_container:
            all_jobs = all_jobs_container.find_all("li")
            for job in all_jobs:
                job_data = {}

                # Extract job ID
                job_data["Job-id"] = job.get('data-jobid')

                # Extract company name
                company_div = job.find("span", class_="EmployerProfile_compactEmployerName__LE242")
                job_data["name-of-company"] = company_div.get_text(strip=True) if company_div else ''

                # Extract job name and URL
                job_link = job.find("a", class_="JobCard_jobTitle___7I6y")
                job_data["name-of-job"] = job_link.get_text(strip=True) if job_link else ''
                job_data["Job-URL"] = job_link.get('href') if job_link else ''

                # Extract location
                location_div = job.find("div", class_="JobCard_location__rCz3x")
                job_data["location"] = location_div.get_text(strip=True) if location_div else ''

                # Extract salary
                salary_div = job.find("div", class_="JobCard_salaryEstimate__arV5J")
                job_data["salary"] = salary_div.get_text(strip=True) if salary_div else ''

                # Extract skills
                description_div = job.find("div", class_="JobCard_jobDescriptionSnippet__yWW8q")
                if description_div:
                    divs = description_div.find_all("div")
                    skills_div = divs[1] if len(divs) > 1 else None
                    job_data["skills"] = skills_div.get_text(strip=True).replace("Skills:", "").strip() if skills_div else ''
                else:
                    job_data["skills"] = ''

                jobs_list.append(job_data)

            # Check and close the modal if it appears
            close_modal_if_present()

            # Try to click the "Load More" button
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='load-more']"))
                )
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                # Ensure button is not blocked
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(3)  # Wait for new content to load
            except Exception as e:
                print(f"No more load more button or error: {e}")
                break  # Break if there is any issue with finding or clicking the button

finally:
    driver.quit()

# Convert the list to a DataFrame
df = pd.DataFrame(jobs_list)
# Save the DataFrame to a CSV file
df.to_csv('scraped_glassdoor_job_file.csv', index=False, encoding='utf-8')
