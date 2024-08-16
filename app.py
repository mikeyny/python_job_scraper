import requests
from bs4 import BeautifulSoup
import csv

# Initialize a list to store job details
job_listings = []

# Initialize the URL for the job listings
url = 'https://www.python.org/jobs/'

while url:
    # Send a GET request to fetch the content of the page
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the list of job postings
    jobs_list = soup.find('ol', class_='list-recent-jobs')

    # Iterate through each job posting and extract relevant details
    for job in jobs_list.find_all('li'):
        job_title = job.find('a').text.strip()
        company = job.find('span', class_='listing-company-name').text.strip()
        location = job.find('span', class_='listing-location').text.strip()
        posted_date = job.find('time').text.strip()
        job_link = job.find('a')['href']  # Extract the job link
        
        # Append the job details to the list
        job_listings.append({
            'Job Title': job_title,
            'Company': company,
            'Location': location,
            'Posted': posted_date,
            'Link': job_link 
        })

    # Find the next page element
    next_page = soup.find('li', class_='next')
    # Check if the next page exists and get the URL
    url = f'https://www.python.org/jobs{next_page.find("a")["href"]}' if next_page and next_page.find("a")["href"] else None

# Save all job details to a CSV file at the end
with open('job_listings.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Job Title', 'Company', 'Location', 'Posted','Link']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write all job listings to the CSV file
    for job in job_listings:
        writer.writerow(job)