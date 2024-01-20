from collections import Counter
import pandas as pd

liston=['INSERT LIST OF PUBLISHERS']

results=dict()
lista=Counter(liston)
for element, count in lista.items():
     percentage=(count/len(liston))*100
     results[str(element)]=float(percentage)

print(sorted(results.items(), key=lambda x: x[1]))