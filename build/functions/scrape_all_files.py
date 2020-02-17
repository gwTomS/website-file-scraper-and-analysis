import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager(1)
html = http.request('GET', 'http://google.com').data

soup = BeautifulSoup( html, 'html.parser' )

for link in soup.findAll('a'):
    print(link.get('href'))
