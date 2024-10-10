from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.psx.com.pk/psx/resources-and-tools/listings/listed-companies")

# Wait for page to load
wait = WebDriverWait(driver, 10)

# Function to scrape data from each company's modal
def scrape_company_data():
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
            
    # Print the extracted data
    print("Company Data:", data)
    return data

# Function to scrape data specifically for the "Automobile assembler" sector
def scrape_psx_data():
    sector_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "sector"))))
    
    # Select the "Automobile assembler" sector by value
    sector_dropdown.select_by_value("0805")
    time.sleep(2)  # Allow time for the table to load
    
    # Get the list of companies in the selected sector
    companies = driver.find_elements(By.CLASS_NAME, "addressbook")
    
    for company in companies:
        company_name = company.text.strip()  # Get the name of the company
        
        try:
            company.click()  # Click to open the modal
            time.sleep(2)  # Wait for modal to load
            scrape_company_data()  # Extract and print company data
            
            # Safely close the modal
            close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "close")))
            close_button.click()  # Close the modal
            
        except Exception as e:
            print(f"Error with company {company_name}: {e}")
            # Continue to the next company in the loop

        time.sleep(1)  # Wait before moving to the next company

# Start scraping
scrape_psx_data()

# Close the driver when done
driver.quit()
