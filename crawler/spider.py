from bs4 import BeautifulSoup
import requests


# First spider designed to crawl only mangareader (maybe add more sources later)
base_url = 'https://www.mangareader.net'
alphabetic_list = '/alphabetical'

http_return = requests.get(base_url + alphabetic_list)
soup = BeautifulSoup(http_return.content, 'lxml')
series_columns = soup.find_all('div', {"class": "series_col"})

series_array = []
for column in series_columns:
    lists = column.find_all('li')
    for series in lists:
        series_name = series.text if series.text[0] != ' ' else series.text[1::]
        series_tuple = series_name, series.find('a')['href']
        series_array.append(series_tuple)
series_array.sort()

# TODO add function to save in database for further usage of data
print(series_array)
