import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import xlsxwriter
from requests import get


doislist=list()
dois = pd.read_excel('filtered.xlsx', usecols = 'S')
for i, row in dois.iterrows():

        doislist.append(row["dc.identifier.doi[en_US]"])
    
listaocindex=list()
for i in doislist:
    API_CALL = "https://opencitations.net/index/api/v2/citation-count/doi:"+i
    HTTP_HEADERS = {"accept": "application/json"}

    try:
        listaocindex.append(int(get(API_CALL, headers=HTTP_HEADERS).json()[0]["count"]))
    except Exception as e:
        listaocindex.append(0)

listaocindex.insert(0,"cited_by_oc")
workbook = xlsxwriter.Workbook('resultsoc.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet1.write_column('A1', listaocindex)
workbook.close()
print (listaocindex)
