import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import xlsxwriter


urlslist=list()
urls = pd.read_excel('filtered.xlsx', usecols = 'Z')
for i, row in urls.iterrows():

        urlslist.append(row["dc.identifier.uri"])
    
listascopusindex=list()
for i in urlslist:
    url=str(i)
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the value based on HTML structure and tags
        try:
            value_to_extract = soup.find('div', class_="metric-counter-scopus").text
            listascopusindex.append(int(value_to_extract.replace('\t', '').replace('\n', '')))
            # Print the extracted value
            print(int(value_to_extract.replace('\t', '').replace('\n', '')))         
        except Exception as e:
            listascopusindex.append(0)
        
        
    else:
        print(f"Failed to retrieve the webpage. Status Code: {response.status_code}")

print (listascopusindex)
listascopusindex.insert(0,"cited_by_scopus")
workbook = xlsxwriter.Workbook('INSERT EXCEL OUTPUT FILE NAME HERE')
worksheet1 = workbook.add_worksheet()
worksheet1.write_column('A1', listascopusindex)
workbook.close()