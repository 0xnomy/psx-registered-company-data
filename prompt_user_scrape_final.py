from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import openpyxl
import os

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.psx.com.pk/psx/resources-and-tools/listings/listed-companies")

# Wait for page to load
wait = WebDriverWait(driver, 10)

# Function to save data to Excel
def save_to_excel(df, file_name):
    if not os.path.exists(file_name):
        # If file does not exist, create it with the data
        df.to_excel(file_name, index=False, engine='openpyxl')
    else:
        # If file exists, append the data without overwriting
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

# Function to scrape data from each company's modal
def scrape_company_data(file_name):
    retries = 3  # Number of retries
    while retries > 0:
        try:
            # Wait for the modal to load and scrape the data
            modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-body")))
            soup = BeautifulSoup(modal.get_attribute("innerHTML"), "html.parser")  # Get modal HTML content
            
            # Extract the relevant data
            data = {}
            for row in soup.find_all("tr"):
                columns = row.find_all("td")
                if len(columns) == 2:  # Ensure there are two columns to extract data
                    key = columns[0].get_text(strip=True)
                    value = columns[1].get_text(strip=True)
                    data[key] = value
            
            # Convert the data dictionary to a pandas DataFrame
            df = pd.DataFrame([data])
            
            # Append the data to the Excel file
            save_to_excel(df, file_name)
            
            return True  # If scraping is successful, return True to indicate success
        
        except Exception as e:
            retries -= 1
            print(f"Error while scraping company data: {e}. Retries left: {retries}")
            time.sleep(2)  # Wait a little before retrying
    
    return False  # Return False if it fails after all retries

# Function to scrape data for the selected sector
def scrape_psx_data(sector_index, file_name):
    sector_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "sector"))))
    
    # Get all options from the dropdown
    options = sector_dropdown.options
    
    # Select the sector by user choice
    sector_name = options[sector_index].text.strip()  # Get the sector name
    print(f"Scraping sector: {sector_name}")
    
    # Select the sector
    sector_dropdown.select_by_visible_text(sector_name)
    time.sleep(2)  # Allow time for the table to load
    
    # Get the list of companies in the selected sector
    companies = driver.find_elements(By.CLASS_NAME, "addressbook")
    
    for company in companies:
        company_name = company.text.strip()  # Get the name of the company
        print(f"Scraping company: {company_name}")
        
        retries = 3  # Number of retries for clicking and scraping each company
        while retries > 0:
            try:
                # Scroll the company element into view
                driver.execute_script("arguments[0].scrollIntoView();", company)
                
                # Wait for the element to be clickable
                wait.until(EC.element_to_be_clickable(company))
                
                # Use JavaScript to force-click the company
                driver.execute_script("arguments[0].click();", company)
                time.sleep(2)  # Wait for modal to load
                
                if scrape_company_data(file_name):  # Try to scrape company data
                    print(f"Successfully scraped data for {company_name}")
                    # Safely close the modal
                    close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "close")))
                    close_button.click()  # Close the modal
                    break  # Exit the retry loop if successful
                
            except Exception as e:
                print(f"Error with company {company_name}: {e}. Retries left: {retries}")
                retries -= 1
                time.sleep(2)  # Wait before retrying

                # Refetch the company element in case the page updated
                companies = driver.find_elements(By.CLASS_NAME, "addressbook")
                company = companies[companies.index(company)]  # Refetch the specific company element
            
        # If after retries, the company data is not scraped, log it and continue to the next company
        if retries == 0:
            print(f"Failed to scrape data for company {company_name} after multiple attempts.")
        
        time.sleep(1)  # Wait before moving to the next company

# Prompt the user to select a sector
sector_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "sector"))))
options = sector_dropdown.options
print("Available sectors:")
for i, option in enumerate(options[1:], start=1):  # Skip the first placeholder
    print(f"{i}: {option.text.strip()}")

# Ask the user for the sector number and file name
sector_choice = int(input("Enter the number of the sector to scrape: "))
file_name = input("Enter the file name to save the data (with .xlsx extension): ")

# Start scraping the selected sector
scrape_psx_data(sector_choice, file_name)

# Close the driver when done
driver.quit()

print(f"Scraping completed. Data saved to '{file_name}'.")
