import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import xlsxwriter
from requests import get
from collections import Counter

def counttypes():
     pubtype=pd.read_excel('filtered.xlsx', usecols = 'BA')
     citationsoc = pd.read_excel('filtered.xlsx', usecols = 'BI')
     citationsscopus = pd.read_excel('filtered.xlsx', usecols = 'BG')
     pubs=list()
     for i, row in pubtype.iterrows():
          if (citationsoc.loc[i]['cited_by_oc']-citationsscopus.loc[i]['cited_by_scopus'])>0:
               pubs.append(row[0])

     results=dict()
     lista=Counter(pubs)
     for element, count in lista.items():
          percentage=(count/len(pubs))*100
          results[str(element)]=float(percentage)

     print(sorted(results.items(), key=lambda x: x[1]))
     return(sorted(results.items(), key=lambda x: x[1]))
    
