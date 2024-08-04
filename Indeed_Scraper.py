# Program to Scrape Job Information from Indeed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time

# Define query and location variables
query = "data analyst"
location = "Canada"

# Construct the base URL using query and location
base_url = f"https://ca.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}&filter=0&sort=date&start="

# Set up the WebDriver service and options
service = Service() 
options = webdriver.ChromeOptions()
# Uncomment the next line to run Chrome in headless mode
# options.add_argument("--headless")
options.add_argument("--incognito")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

job_lst = []  # List to store job details

start = time.time()  # Start the timer

try:
    # Fetch the first page
    driver.get(base_url + "0")
    
    # Wait until the job count element is visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "jobsearch-JobCountAndSortPane-jobCount"))
    )

    # Determine the total number of pages
    try:
        count_text = driver.find_element(By.CLASS_NAME, 'jobsearch-JobCountAndSortPane-jobCount').text
        max_iter_pgs = int(count_text.replace('+', '').replace(',', '').split(' ')[0]) // 15
    except NoSuchElementException:
        max_iter_pgs = 1  # Default to 1 page if count not found

    # Iterate through all pages
    for i in range(max_iter_pgs):
        url = base_url + str(i * 10)
        driver.get(url)

        # Wait for the job results to be visible
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "mosaic-jobResults"))
            )
        except TimeoutException:
            continue  # Skip this page if it times out
        
        # Extract job postings
        job_page = driver.find_element(By.ID, "mosaic-jobResults")
        jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for job in jobs:
            try:
                # Extract job title and URL
                job_title_element = job.find_element(By.CLASS_NAME, "jobTitle")
                job_title = job_title_element.text
                job_href = job_title_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                job_id = job_title_element.find_element(By.CSS_SELECTOR, "a").get_attribute("id")

                # Extract company name, location, and salary
                try:
                    company_name = job.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name"]').text
                except NoSuchElementException:
                    company_name = None

                try:
                    location = job.find_element(By.CSS_SELECTOR, 'div[data-testid="text-location"]').text
                except NoSuchElementException:
                    location = None

                try:
                    salary_container = job.find_element(By.CLASS_NAME, 'salary-snippet-container')
                    salary = salary_container.find_element(By.CSS_SELECTOR, 'div[data-testid="attribute_snippet_testid"]').text
                except NoSuchElementException:
                    salary = None

                # Append job details to the list
                job_lst.append([job_title, job_href, job_id, company_name, location, salary])

            except NoSuchElementException:
                continue  # Skip this job if any detail is missing

finally:
    # Close the WebDriver
    driver.quit()

# Create a DataFrame from the list of job details
df = pd.DataFrame(job_lst, columns=['Title', 'URL', 'Job ID', 'Company Name', 'Location', 'Salary'])

# Save the DataFrame to a CSV file
df.to_csv('scraped_job_file.csv', index=False, encoding='utf-8')

end = time.time()  # End the timer
print(f"Completed in {end - start} seconds!")
