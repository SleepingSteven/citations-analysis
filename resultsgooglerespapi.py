from google_scholar_py import SerpApiGoogleScholarOrganic
import json
import pandas as pd 
import xlsxwriter

citationcountd=dict()
citationcountl=list()
DOIs = pd.read_excel('filtered.xlsx', usecols = 'S')
doilist=list()
for i, row in DOIs.iterrows():
    if pd.isna(row["doi"]):
        pass
    else: 
        doilist.append(row["doi"])

parser = SerpApiGoogleScholarOrganic()

for i in doilist:

    try:
        data = parser.scrape_google_scholar_organic_results(
            query=i,
            api_key="INSERT SERPAPI KEY HERE",
            pagination=False,
        )
        try:
            citationcountd[i]=data[0]["inline_links"]["cited_by"]["total"]
            citationcountl.append(data[0]["inline_links"]["cited_by"]["total"])
        except KeyError as e:
            citationcountd[i]=0
            citationcountl.append(0)
        except Exception as e:
            citationcountd[i]=0
            citationcountl.append(0)
    except Exception as e:
        citationcountd[i]=0
        citationcountl.append(0)
    

print (citationcountl)


lista=list()

citationcountl.insert(0,"cited_by_google")
workbook = xlsxwriter.Workbook('INSERT EXCEL OUTPUT FILE NAME HERE')
worksheet1 = workbook.add_worksheet()
worksheet1.write_column('A1', citationcountl)
workbook.close()


