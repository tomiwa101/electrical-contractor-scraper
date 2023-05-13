### Web Scraper for Florida Electrical Contractors Licenses
This Python script uses the Selenium library to automate web scraping of the Florida Department of Business and Professional Regulation website. Specifically, it scrapes the page for electrical contractor licenses, which includes data such as license numbers, company names, and contact information.

## Requirements
Python 3.6+
Selenium library
webdriver-manager library
Scrapy library
## Installation
- Clone this repository to your local machine using git clone ..... git url
- In the project directory, run pip install -r requirements.txt to install the necessary libraries.
## Usage
- Open the app.py file in a code editor of your choice.
- Customize the script by modifying the selections dictionary to reflect the search parameters you want to use.
- Save the file and run it using python app.py.
The script will automate the web scraping process and print out the results to the console.
 
## Customization
The selections dictionary in app.py contains the following keys:
- Board: The type of board to search for. (Default: 'Electrical Contractors')
- LicenseType: The type of license to search for. (Default: 'Cert. Electrical Contractors (EC)')
- County: The name of the county to search for. (Default: 'Dade')
- State: The state to search in. (Default: 'Florida')
- RecsPerPage: The number of records to display per page. (Default: '50')
You can modify the values of these keys to customize the search parameters.
 
## Output
The script will print out the results of the web scraping process to the console. The data will be organized into a dictionary with the following keys:

- License Number
- Business Name
- County
- Phone
- Email
- Website
- Status
- Expires
- Insurance
  
## License
This project is licensed under the terms of the MIT license.
