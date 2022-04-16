#TODO:
#create sys arg to pass in site to crawl
#add headers to identify crawler
#set rate for spider to allow for responsbile crawl
#create output as xml sitemap

from bs4 import BeautifulSoup
import requests
import sys

import xml.etree.ElementTree as ET
from datetime import datetime

headers = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

#URL to crawl, can be passed to script -> python crawl-create-sitemap.py "ADD-URL-HERE-TO-CRAWL-HERE"
url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.jasonclark.info'
domain = url.split('/')[2]
#print('Scraping results for "'+url+'"')
print('Scraping results for "'+domain+'"')

params = {
  #"q": "msu library",
  #"directory": "/news"
}

pages_crawled = []

#def crawler(url, headers, params):
def crawler(url, headers):
  #page = requests.get(url, params=params, headers=headers)
  page = requests.get(url, headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')
  links = soup.find_all('a')

  for link in links:
    if 'href' in link.attrs:
      #if link['href'].startswith('/wiki') and ':' not in link['href']:
      #if link['href'].startswith('/') and ':' not in link['href']:
        if link['href'] not in pages_crawled:
          #new_link = f"https://en.wikipedia.org{link['href']}"
          new_link = f"{url}.{link['href']}"
          pages_crawled.append(link['href'])
          print(*pages_crawled, sep = "\n")

          dt = datetime.now().strftime("%Y-%m-%d")  # <-- Get current date and time.
          schema_loc = ("http://www.sitemaps.org/schemas/sitemap/0.9"
                  "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

          root = ET.Element("urlset")
          root.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
          root.attrib['xsi:schemaLocation'] = schema_loc
          root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

          for i in range(len(pages_crawled)):
            doc = ET.SubElement(root, "url")
            #ET.SubElement(doc, "loc").text = f"{url.pages_crawled[i]}"
            ET.SubElement(doc, "loc").text = pages_crawled[i]
            ET.SubElement(doc, "lastmod").text = dt
            ET.SubElement(doc, "changefreq").text = 'weekly'
            ET.SubElement(doc, "priority").text = "0.8"
          tree = ET.ElementTree(root)
          
          print('Writing out xml and csv files.')          
          
          try:
            tree.write('./outputs/sitemap-'+domain+'.xml', encoding='utf-8', xml_declaration=True)
          except:
            continue          

          try: 
            with open('./outputs/sitemap-'+domain+'.csv', 'a') as file:
              #file.write(f'{soup.title.text}; {link.text}; {link["href"]}\n')
              file.write(f'{link.text}, {link["href"]}\n')
              crawler(new_link)
          except:
            continue
                           
#crawler('https://en.wikipedia.org', headers)
crawler(url, headers)
