import urllib3
from bs4 import BeautifulSoup

def get_base_url(url):
    return url.rsplit('/', 1)[0]

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

    if 'Content-Disposition' in str( header ):
        filename = './' + html.info()['Content-Disposition'].split( '=' )[-1].strip( '"' )
        file_names.append(filename)

    return file_names

def download_files(file_path, base_url):
    file_url = base_url + file_path

    f = connection.request('GET', file_url).data.read()

    with open('./images/' + file_path, "wb") as code:
            code.write(f)


connection = urllib3.PoolManager(1)

url = 'https://glasswallsolutions.com/'
base_url = get_base_url(url)

page_links = get_all_links_from_url(url, connection)

first_page_filenames = get_all_files_on_page(page_links[0])

download_files(first_page_filenames[0], base_url)





# print(f'\nInternal Links in https://glasswallsolutions.com/.\n' + '='*100)
# for link in page_links:
#     print(link)
