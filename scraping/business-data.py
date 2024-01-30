# Group 1 project - Data Scraping code
import requests
from bs4 import BeautifulSoup
import csv
import logging
import os  # Import the os module

# Configure the logging module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Base URL for the pages with pagination
base_url = "https://disfold.com/world/companies"
page_number = 3  # Start with page 1

# Define the CSV filename
csv_filename = 'top_companies.csv'

# Initialize a flag to determine if the CSV file needs headers
write_headers = not os.path.exists(csv_filename)  # Check if the file exists using os.path.exists()

while True:
    # Create the URL for the current page
    url = base_url if page_number == 0 else f"{base_url}/?page={page_number}"

    # Send an HTTP GET request to the current page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing the data
        table = soup.find('table', class_='striped')

        # Check if the table exists on the page
        if table:
            # Initialize a list to store the data for the current page
            data = []

            # Iterate through the rows of the table
            for row in table.find('tbody').find_all('tr'):
                # Extract data from each cell in the row
                columns = row.find_all('td')
                
                # Check if the row has enough columns
                if len(columns) >= 7:
                    ranking = columns[0].text.strip()
                    company = columns[1].find('a').text.strip()

                    market_cap_cell = columns[2].find('a')
                    if market_cap_cell:
                        market_cap = market_cap_cell.text.strip()
                    else:
                        market_cap = columns[2].text.strip()

                    # Handle stock cell
                    stock_cell = columns[3].find('a')
                    if stock_cell:
                        stock = stock_cell.text.strip()
                    else:
                        stock = columns[3].text.strip()
                    
                    # Handle country cell
                    country_cell = columns[4].find('a')
                    if country_cell:
                        country = country_cell.text.strip()
                    else:
                        country = columns[4].text.strip()
                    
                    # Handle sector cell
                    sector_cell = columns[5].find('a')
                    if sector_cell:
                        sector = sector_cell.text.strip()
                    else:
                        sector = columns[5].text.strip()
                    
                    # Handle industry cell
                    industry_cell = columns[6].find('a')
                    if industry_cell:
                        industry = industry_cell.text.strip()
                    else:
                        industry = columns[6].text.strip()


                    # Append the extracted data as a list to the data list for the current page
                    data.append([ranking, company, market_cap, stock, country, sector, industry])

            # Append the data from the current page to the CSV file
            with open(csv_filename, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                if write_headers:
                    # Write the header row if the file is newly created
                    csv_writer.writerow(['Ranking', 'Company', 'Market Cap (USD)', 'Stock', 'Country', 'Sector', 'Industry'])
                    write_headers = False  # Headers have been written
                # Write the data rows
                csv_writer.writerows(data)

            # Log the progress
            logging.info(f'Scraped data from page {page_number}')

            # Increment the page number for the next iteration
            page_number += 1
        else:
            # No more pages to scrape, break the loop
            break
    else:
        logging.error(f'Failed to retrieve page {page_number} (Status Code: {response.status_code})')
        break

logging.info(f'Data from all pages saved to {csv_filename}')
