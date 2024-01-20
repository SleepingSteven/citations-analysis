from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import xlsxwriter
import re
import time
from collections import Counter
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from google_scholar_py import CustomGoogleScholarOrganic
import json

def find(id):
    risultati=list()
    
    url="https://www.scopus.com/results/citedbyresults.uri?sort=plf-f&cite="+str(id)+"&src=s&imp=t&sid=33e1ec4a5f48dff43a7ff7fa9bb4cbdb&sot=cite&sdt=a&sl=0&origin=inward&editSaveSearch=&txGid=1ca3531392a86ff29ae72f4d43b343d0"
    options = webdriver.ChromeOptions() 
    #set driver options and chrome profile to avoid log in pages 
    options.add_argument("user-data-dir=ADD PATH TO CHROME DIRECTORY WITH PROFILES")
    options.add_argument("profile-directory=Profile 1")
    options.add_argument("--disable-extensions")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(10)
    driver.get(url)
    driver.set_page_load_timeout(15)

    # Check if login was successful (you might need to customize this based on the website)
   
    print("ok")
    
    if True:
    # Parse the HTML content of the webpage
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the value based on HTML structure and tags
        try:
            values_to_extract = soup.find_all('span', class_="docTitle")

            for i in values_to_extract:
                    risultati.append((((i.text).replace('\t', '').replace('\n', '').replace('\xa0',''))).lower())
                    

        except Exception as e:
            risultati=[]
            print ("none")

        
    else:
        print(f"Failed to retrieve the webpage. Status Code: {response.status_code}")
    return risultati

API_CALL = "https://opencitations.net/meta/api/v1/metadata/doi:"
HTTP_HEADERS = {"accept": "application/json"}



listonescopus=list()
listoneoc=list()
dois = pd.read_excel('filtered4.xlsx', usecols = 'S')
indexscopus = pd.read_excel('filtered4.xlsx', usecols = 'BG')
indexoc = pd.read_excel('filtered4.xlsx', usecols = 'BI')
scopusid= pd.read_excel('filtered4.xlsx', usecols = 'W')
citazioniscopus=list()
citazionioc=list()
publishersnotinscopus=list()
publishersnotinoc=list()

for i, row in dois.iterrows():
    citazioniscopus=list()
    citazionioc=list()
    doislist=list()
    result=list()
    if (indexoc.loc[i]['cited_by_oc']-indexscopus.loc[i]['cited_by_scopus'])>0:

        citazioniscopus=find(scopusid.loc[i]['dc.identifier.other'])
        for j in requests.get("https://opencitations.net/index/api/v2/citations/doi:"+dois.loc[i]['dc.identifier.doi[en_US]'], headers=HTTP_HEADERS).json():
            ids=j["citing"].split()
            for h in ids:
                    if "doi:" in h:
                        doislist.append((h.replace('doi:','')))
        
        for j in doislist:
            
            try:
                citazionioc.append((requests.get(API_CALL+j, headers=HTTP_HEADERS).json()[0]["title"]).lower())
            except Exception as e:
                                pass
        for j in citazionioc:
                
                if j not in citazioniscopus:
                    result.append(j)
        print ("Difference for DOI: "+dois.loc[i]['dc.identifier.doi[en_US]']+": ")
        print(result)
        for i in result:
            successful=False
            while not successful:
                try:
                    parser = CustomGoogleScholarOrganic()
                    data = parser.scrape_google_scholar_organic_results(
                        query=i,
                        pagination=False,
                        save_to_csv=False,
                        save_to_json=False
                    )
                    if "publication_info" in data[0]:
                        try:
                            print((data[0]["publication_info"].split(" - "))[1])
                            successful=True
                            publishersnotinscopus.append((data[0]["publication_info"].split(" - "))[1])
                            print (publishersnotinscopus)
                        except Exception as b:
                            successful=True
                            print("Ok but formatting error")
                    elif data:
                            successful=True
                            print("Ok but formatting error")
                except Exception as e:
                    print("failed")
                    time.sleep(5)
        pass

    elif (indexscopus.loc[i]['cited_by_scopus']-indexoc.loc[i]['cited_by_oc'])>=0: 

        citazioniscopus=find(scopusid.loc[i]['dc.identifier.other'])
        for j in requests.get("https://opencitations.net/index/api/v2/citations/doi:"+dois.loc[i]['dc.identifier.doi[en_US]'], headers=HTTP_HEADERS).json():
            ids=j["citing"].split()
            for h in ids:
                    if "doi:" in h:
                        doislist.append((h.replace('doi:','')))
        
        for j in doislist:
            
            try:
                citazionioc.append((requests.get(API_CALL+j, headers=HTTP_HEADERS).json()[0]["title"]).lower())
            except Exception as e:
                                pass
        for j in citazioniscopus:
                
                if j not in citazionioc:
                    result.append(j)
        print ("Difference for DOI: "+dois.loc[i]['dc.identifier.doi[en_US]']+": ")
        print(result)
        for i in result:
            successful=False
            while not successful:
                try:
                    parser = CustomGoogleScholarOrganic()
                    data = parser.scrape_google_scholar_organic_results(
                        query=i,
                        pagination=False,
                        save_to_csv=False,
                        save_to_json=False
                    )
                    if "publication_info" in data[0]:
                        try:
                            print((data[0]["publication_info"].split(" - "))[1])
                            successful=True
                            publishersnotinoc.append((data[0]["publication_info"].split(" - "))[1])
                            print (publishersnotinoc)
                        except Exception as b:
                            successful=True
                            print("Ok but formatting error")
                    elif data:
                            successful=True
                            print("Ok but formatting error")
                except Exception as e:
                    print("failed")
                    time.sleep(10)
        pass
    

print(publishersnotinoc)
print(publishersnotinscopus)






