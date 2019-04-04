"""
Scrapes last name data.  Data source is https://names.mongabay.com/most_common_surnames.htm
Another useful resources for countries other than the US: https://www.quora.com/If-a-large-group-of-people-are-divided-by-last-name-A-M-and-N-Z-will-you-get-a-50-50-distribution
"""

import numpy as np
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs

# The number scheme for the pages is rediculous
base_url = 'https://names.mongabay.com/most_common_surnames{}.htm'
page_numbers = ['', '1', '5', '8', '12', '16']
datadict = None
for n in page_numbers:
    print('on:', n)
    res = req.get(base_url.format(n))
    soup = bs(res.content, 'lxml')
    table = soup.find('table')
    rows = table.find_all('tr')

    if datadict is None:
        datadict = {}
        # assumes labels are the same on every page
        labels = [t.text for t in rows[0].find_all('th')]
        for l in labels:
            datadict[l] = []

    data = []
    for r in rows[1:]:
        data.append([t.text for t in r.find_all('td')])

    data = np.array(data)

    for i, l in enumerate(labels):
        datadict[l].extend(data[:, i])

# convert numeric columns from strings to numeric datatypes
df = pd.DataFrame(datadict)
for c in ['ApproximateNumber', '%Frequency', 'Rank']:
    df[c] = pd.to_numeric(df[c].str.replace(',', ''))

df.sort_values(by='Surname', inplace=True, ascending=True)
df['Percent'] = df['ApproximateNumber'] / df['ApproximateNumber'].sum()
df['Cumulative_percent'] = df['Percent'].cumsum()

# save df as csv
df.to_csv('cumulative_percent_surnames.csv', index=False)
