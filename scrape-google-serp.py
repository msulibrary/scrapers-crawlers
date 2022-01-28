import requests, lxml, sys
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

headers = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

#query string to search, can be passed to script -> python scrape-google-serp.py "ADD-QUERY-HERE-IN-QUOTES-IF-MULTIPLE-WORDS"
q = sys.argv[1] if len(sys.argv) > 1 else 'msu library'
print('Scraping results for "'+q+'"')

params = {
  "q": q,
  #"q": "msu library",
  "hl": "en",
  "gl": "us",
  "num": "25",
}

html = requests.get("https://www.google.com/search", params=params, headers=headers)
if html.status_code == 200:
  soup = BeautifulSoup(html.text, 'lxml')
  #soup = BeautifulSoup(html.text, 'html.parser')

results = []
for item in soup.find_all('div', class_='g'):
  anchors = item.find_all('a')
  if anchors:
    link = anchors[0]['href']
    #link = item.find('cite').text
    try: breadcrumbs = item.find('cite').text
    except AttributeError: breadcrumbs = 'breadcrumbs not available during this crawl'
    try: title = item.find('h3').text
    except AttributeError: title = 'title not available during this crawl'
    #description = item.find('a').text
    try: description = item.select_one('.IsZvec').text
    except AttributeError: description = 'description not available during this crawl'
    entry = {
      "title": title,
      "link": link,
      "breadcrumbs": breadcrumbs,
      "description": description
    }
    results.append(entry)
print(results)

df = pd.DataFrame(results)
query = params['q'].replace(" ", "-")
#now = datetime.today().isoformat()
#now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
now = datetime.today().strftime('%Y-%m-%d')
columns = ['title', 'link', 'breadcrumbs', 'description']
df.to_csv('./data/google-serp-snapshot-'+query+'-'+now+'.csv', encoding='utf-8', index=False, header=columns)  
print('Your data has been saved successfully.\n')

#for results in soup.select('.g'):
  #title = results.select_one('h3').text
  #link = results.select_one('cite').text
  #description = results.select_one('a').text
  #description = results.select_one('.IsZvec').text
  #print(f'{title}\n{link}\n{description}\n')
  #results.append({
    #"title": title, "url": link, "description": description
  #}, ignore_index=True)

#df = pd.DataFrame(results)
#df.to_csv('serp-snapshot.csv', encoding='utf-8', index=False, header=False)  
#print('Your data has been saved successfully.\n')

#df = pd.DataFrame(result)
#now = datetime.now()
#outputFileName = 'SearchOutput' + now.strftime("%d-%m-%Y") + '.csv'
# Write output in CSV format.
#df.to_csv(outputFileName,mode='a', encoding='utf-8', index=False , header=False)
#print('Your data has been saved successfully.\n')
