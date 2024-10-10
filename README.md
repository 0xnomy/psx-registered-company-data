# PSX Listed Companies Data Scraper

This repository contains data scraped from the **Pakistan Stock Exchange (PSX)**, the primary stock exchange in Pakistan where companies from various sectors are listed for trading. The PSX hosts companies from a wide range of industries, providing essential information about each listed entity.

The data includes detailed contact and registration information for representatives from these companies. This repository also contains the Python code used to scrape the data, making it easy to collect updated information in the future.

## About the PSX
The **Pakistan Stock Exchange (PSX)** is a platform where companies list their shares for public trading. Companies across many sectors such as banking, energy, textiles, and manufacturing are listed on the PSX, and their stock performance reflects the overall health and economic trends of these industries in Pakistan.

## Scraped Data

The data scraped from the PSX website includes important details of company representatives across various sectors. The following information is captured for each listed company:

- **Representative**: Name of the company representative
- **Designation**: Representative's role within the company
- **Company**: Name of the listed company
- **Address**: The company's official address
- **Phone**: Primary contact number
- **Phone 2**: Secondary contact number (if available)
- **Fax**: Fax number (if available)
- **Date of Listing**: The date the company was listed on PSX
- **Email**: Contact email address
- **URL**: Company website URL
- **Registrar Details**: Information on the registrar handling the company's shares

### Sectors from which data was extracted:

1. Automobile Assembler
2. Automobile Parts & Accessories
3. Cable & Electrical Goods
4. Cement
5. Chemical
6. Close-end Mutual Fund
7. Commercial Banks
8. Engineering
9. Exchange Traded Funds
10. Fertilizer
11. Food & Personal Care Products
12. Glass & Ceramics
13. Insurance
14. Investment Banks / Investment Companies / Securities Companies
15. Jute
16. Leasing Companies
17. Leather & Tanneries
18. Miscellaneous
19. Modarabas
20. Oil & Gas Exploration Companies
21. Oil & Gas Marketing Companies
22. Paper, Board & Packaging
23. Pharmaceuticals
24. Power Generation & Distribution
25. Property
26. Real Estate Investment Trust
27. Refinery
28. Sugar & Allied Industries
29. Synthetic & Rayon
30. Technology & Communication
31. Textile Composite
32. Textile Spinning
33. Textile Weaving
34. Tobacco
35. Transport
36. Vanaspati & Allied Industries
37. Woollen

### Sectors without extractable data:
- Bonds
- Stock Index Future Contracts
- Future Contracts

## Code

The Python code in this repository automates the scraping process from the PSX website. It navigates the dropdown menus for different sectors, extracts company details, and saves the information in a structured format .xlsx for easy analysis and access.

## Usage

To scrape the data, you will need to have **Selenium WebDriver** installed, along with a browser driver (ChromeDriver). Web scraping libraries like **BeautifulSoup** and data processing tools like **Pandas** are also used.

### Required Dependencies:

Install the following dependencies
```bash
selenium
webdriver-manager
beautifulsoup4
pandas
openpyxl
```

### Additional Setup

1. **WebDriver Setup**:  
   The script uses Selenium with Chrome WebDriver to automate the browser for scraping. You'll need to install a web driver for Chrome:
   - **ChromeDriver**: You can install it automatically using `webdriver-manager`:
   ```python
   from selenium import webdriver
   from selenium.webdriver.chrome.service import Service
   from webdriver_manager.chrome import ChromeDriverManager
   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
   ```

2. **Install WebDriver**:
   - Make sure you have **Google Chrome** installed.
   - `webdriver-manager` will take care of downloading the appropriate version of ChromeDriver automatically.

Feel free to open an issue or ask any questions if you encounter problems or need assistance! 
