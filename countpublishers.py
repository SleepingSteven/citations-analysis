from collections import Counter
import pandas as pd

def countpublishers (list):
     liston=lista #list of publishers

     results=dict()
     lista=Counter(liston)
     for element, count in lista.items():
          percentage=(count/len(liston))*100
          results[str(element)]=float(percentage)

     print(sorted(results.items(), key=lambda x: x[1]))
     return(sorted(results.items(), key=lambda x: x[1]))
