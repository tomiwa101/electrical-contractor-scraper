import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from scrapy import Selector
from extractor import extract


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.myfloridalicense.com/wl11.asp?mode=1&SID=&brd=&typ=")

Counties = ['Duval', 'Orange', 'Palm Beach', 'Broward', 'Dade']

selections = {
    'Board': 'Electrical Contractors',
    'LicenseType' : 'Cert. Electrical Contractors (EC)',
    'County': Counties[4],
    'State': 'Florida',
    'RecsPerPage': '50'
}

for key, value in selections.items():
    dropdown = driver.find_element("name", key)
    drop=Select(dropdown)
    drop.select_by_visible_text(value)
    time.sleep(10)

submit = driver.find_element("name", "Search1")
submit.click()

time.sleep(10)

def extr_from_html():
    pageSource = driver.page_source    

    extr = extract(pageSource, selections['County'])
    status = extr.extract_data()



    if status == '200':
        print('succesful')
        main_sel = Selector( text = pageSource )
        page_no = main_sel.xpath("//input[@name = 'Page']/parent::font/text()").get().replace('\n', '').replace('\t', '')
        page_check = [n for n in page_no.split() if n.isnumeric()]
        if page_check[0] != page_check[-1]: 
            submit = driver.find_element("name", "SearchForward")
            submit.click()
            time.sleep(10)
            print(f'extracted page{page_check[0]}')
            extr_from_html()
    else:
        print(status)
        main_sel = Selector( text = pageSource )
        page_no = main_sel.xpath("//input[@name = 'Page']/parent::font/text()").get().replace('\n', '').replace('\t', '')
        page_check = [n for n in page_no.split() if n.isnumeric()]
        print(f'scraping stopped at page{page_check[0]}')

extr_from_html()

print('done')


time.sleep(10)
driver.close()