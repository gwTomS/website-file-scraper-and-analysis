import urllib3
import os
from bs4 import BeautifulSoup
from pathlib import Path

def get_base_url(url):
    return url.rsplit('/', 1)[0]

def path_leaf(path):
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)

def get_all_links_from_url(url, connection):
    base_url = get_base_url(url)

    html = connection.request('GET', url).data
    soup = BeautifulSoup(html, 'html.parser')

    page_links = list()

    for a_tag in soup.findAll('a'):
        link = ''

        if a_tag.get('href').startswith('/'):
            link = base_url + a_tag.get('href')
        elif a_tag.get('href').startswith(base_url):
            link = a_tag.get('href')

        if link != '':
            page_links.append(link)

    return page_links


def get_all_files_on_page(url):
    html = connection.request('GET', url)

    soup = BeautifulSoup(html.data, 'html.parser')

    file_names = list()

    images = soup.findAll('img')
    for image in images:
        file_names.append(image.get('src'))

    header = html.info()

    # TODO: Non image files
    if 'Content-Disposition' in str( header ):
        filename = './' + html.info()['Content-Disposition'].split( '=' )[-1].strip( '"' )
        file_names.append(filename)

    return file_names

def download_file(file_path, base_url, download_path):
    if file_path.startswith('/'):
        file_url = base_url + file_path
    else:
        file_url = file_path

    f = connection.request('GET', file_url).data

    Path(download_path).mkdir(parents=True, exist_ok=True)

    with open(download_path + '/' + path_leaf(file_path), "wb") as code:
            code.write(f)




connection = urllib3.PoolManager(1)

url = 'https://glasswallsolutions.com/'
base_url = get_base_url(url)
base_download_path = './files'

page_links = get_all_links_from_url(url, connection)

for page in page_links:
    print('Processing: ' + page)
    filenames = get_all_files_on_page(page)

    for filename in filenames:
        download_file(filename, base_url, base_download_path)
    
    print('\n')
