import requests
import shutil
from bs4 import BeautifulSoup
import functions
import sys

# TODO make these inputs (web? DJANGO?)
manga_reader_url = 'https://www.mangareader.net/'
manga_folder = 'tmp/'
series = 'one-piece'
chapter = '813'

manga_full_path = manga_folder + series + '/' + chapter + '/'
functions.check_dir(manga_folder)
functions.check_dir(manga_folder + series)
functions.check_dir(manga_full_path)

full_url = manga_reader_url + series + '/' + chapter

last_page = 1
print('Counting how many pages chapter has.')
while requests.get(full_url + '/' + str(last_page + 1)).status_code != 404:
    last_page = last_page + 1
print('This chapter has ' + str(last_page) + ' pages')

for page in range(1, last_page + 1):
    print('Downloading page ' + str(page))
    http_return = requests.get(full_url + '/' + str(page))
    soup = BeautifulSoup(http_return.content, 'lxml')
    img_div = soup.find("div", {"id": "imgholder"}).find("img")['src']

    img_request = requests.get(img_div, stream=True)
    with open(manga_full_path + str(page) + '.jpg', 'wb') as out_file:
        shutil.copyfileobj(img_request.raw, out_file)

