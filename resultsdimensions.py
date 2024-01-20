from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import xlsxwriter
import re
import time


urlslist=list()
urls = pd.read_excel('filtered.xlsx', usecols = 'Z')
for i, row in urls.iterrows():

        urlslist.append(row["dc.identifier.uri"])
    
listascopusindex=list()

    

# Set up the Selenium WebDriver (make sure you have the appropriate driver installed)
  # You can use other browsers as well

for i in urlslist:
    driver = webdriver.Chrome()
    try:
        # Navigate to the webpage
        driver.get(i)

        # Wait for the dynamically loaded content, you may need to adjust the wait time
        time.sleep(2)
        # Find the element using its XPath or other locators
        embedded_element = driver.find_element(By.XPATH, "//div[@class='dimensions']")

        # Access the HTML content of the embedded element
        embedded_element_html = embedded_element.get_attribute('outerHTML')
        soup=BeautifulSoup(embedded_element_html, 'html.parser')
        try:
            value_to_extract = soup.find('div', class_="__db_score_normal").text
            listascopusindex.append(int(value_to_extract.replace('\t', '').replace('\n', '')))
            print (int(value_to_extract.replace('\t', '').replace('\n', '')))
            print ("ok")
        except Exception as e:
            listascopusindex.append(0)
            print (0)
            print("no")
        

    finally:
        # Close the browser
        driver.quit()

print (listascopusindex)
listascopusindex.insert(0,"cited_by_dimensions")
workbook = xlsxwriter.Workbook('INSERT EXCEL OUTPUT FILE NAME HERE')
worksheet1 = workbook.add_worksheet()
worksheet1.write_column('A1', listascopusindex)
workbook.close()