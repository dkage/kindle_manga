import requests
from bs4 import BeautifulSoup


manga_reader_url = 'https://www.mangareader.net/'
series = 'one-piece'
chapter = '813'

full_url = manga_reader_url + series + '/' + chapter
page = 1
print(full_url + '/' + str(page))
http_return = requests.get(full_url + '/' + str(page))
soup = BeautifulSoup(http_return.content, 'lxml')

print(soup)
