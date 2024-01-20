from google_scholar_py import SerpApiGoogleScholarOrganic
import json
import pandas as pd 
from google_scholar_py import CustomGoogleScholarOrganic
import xlsxwriter

citationcountd=dict()
citationcountl=list()
DOIs = pd.read_excel('filtered', usecols = 'S')
doilist=list()
for i, row in DOIs.iterrows():
    if pd.isna(row["dc.identifier.doi[en_US]"]):
        pass
    else: 
        doilist.append(row["dc.identifier.doi[en_US]"])

parser = CustomGoogleScholarOrganic()

lista=list()

for i in doilist:

    try:
        data = parser.scrape_google_scholar_organic_results(
            query=i,
            pagination=False,
            save_to_csv=False,
            save_to_json=False
        )
        try:
            citationcountd[i]=data[0]["cited_by_count"]
            citationcountl.append(data[0]["cited_by_count"])
        except KeyError as e:
            citationcountd[i]=0
            citationcountl.append(0)
        except Exception as e:
            citationcountd[i]=0
            citationcountl.append(0)
    except Exception as e:
        citationcountd[i]=0
        citationcountl.append(0)


citationcountl.insert(0,"cited_by_google")
workbook = xlsxwriter.Workbook('INSERT EXCEL OUTPUT FILE NAME HERE')
worksheet1 = workbook.add_worksheet()
worksheet1.write_column('A1', citationcountl)
workbook.close()

print (citationcountl)



