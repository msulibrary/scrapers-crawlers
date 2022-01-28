import requests, lxml, sys
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

headers = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

#query string to search, can be passed to script -> python scrap-bing-serp.py "ADD-QUERY-HERE-IN-QUOTES-IF-MULTIPLE-WORDS"
q = sys.argv[1] if len(sys.argv) > 1 else 'msu library'
print('Scraping results for "'+q+'"')

params = {
  "q": q,
  #"q": "msu library",
  "setLang": "en",
  #"gl": "us",
  "count": "25",
}

html = requests.get("https://www.bing.com/search", params=params, headers=headers)
if html.status_code == 200:
  soup = BeautifulSoup(html.text, 'lxml')
  #soup = BeautifulSoup(html.text, 'html.parser')

results = []
#results = soup.findAll('li', { "class" : "b_algo" })
#print(results)

for item in soup.find_all('li', class_='b_algo'):
  anchors = item.find_all('a', href=True)
  if anchors:
    link = anchors[0]['href']
    try: breadcrumbs = item.select_one('cite').text
    except AttributeError: breadcrumbs = 'breadcrumbs not available during this crawl'
    try: title = item.select_one('h2').text
    except AttributeError: title = 'title not available during this crawl'
    try: description = item.select_one('p').text
    except AttributeError: description = 'description not available during this crawl'
    entry = {
      "title": title,
      "link": link,
      "breadcrumbs": breadcrumbs,
      "description": description
    }
    results.append(entry)
print(results)

#for item in results:
  #try: title = item.select_one('h2').text
  #except AttributeError: title = 'title not available during this crawl'
  #try: link = item.select_one('h2 > a[href]')
  #except AttributeError: link = 'link not available during this crawl'
  #try: breadcrumbs = item.select_one('cite').text
  #except AttributeError: breadcrumbs = 'breadcrumbs not available during this crawl'
  #try: description = item.select_one('p').text
  #try: description = str(item.select['p']).replace(" ", " ")
  #except AttributeError: description = 'description not available during this crawl'
  #item = {
    #"title": title,
    #"link": link,
    #"breadcrumbs": breadcrumbs,
    #"description": description
  #}
  #results.append(item)
#print(results)

df = pd.DataFrame(results)
query = params['q'].replace(" ", "-")
#now = datetime.today().isoformat()
#now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
now = datetime.today().strftime('%Y-%m-%d')
columns = ['title', 'link', 'breadcrumbs', 'description']
df.to_csv('./data/bing-serp-snapshot-'+query+'-'+now+'.csv', encoding='utf-8', index=False, header=columns)  
print('Your data has been saved successfully.\n')
