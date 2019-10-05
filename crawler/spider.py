from bs4 import BeautifulSoup
import requests


# First spider designed to crawl only mangareader (maybe add more sources later)
base_url = 'https://www.mangareader.net'
alphabetic_list = '/alphabetical'


def grab_all_series():
    http_return = requests.get(base_url + alphabetic_list)
    soup = BeautifulSoup(http_return.content, 'lxml')
    series_columns = soup.find_all('div', {"class": "series_col"})

    series_array = []
    for column in series_columns:
        lists = column.find_all('li')
        for series in lists:
            series_name = series.text if series.text[0] != ' ' else series.text[1::]
            series_tuple = series_name.replace('[Completed]', '').replace(' [Completed]', ''), series.find('a')['href']
            series_array.append(series_tuple)
    series_array.sort()

    return series_array


def get_all_chapters(series_link):
    chapters_array = []
    series_url = base_url + series_link

    http_return = requests.get(series_url)
    soup = BeautifulSoup(http_return.content, 'lxml')
    series_chapters = soup.find('table', {'id': 'listing'}).find_all('tr')

    # Skip first row using 1:: to ignore column headers
    for chapter in series_chapters[1::]:
        # Each row has two TDs, first one contains href and chapter name, second has "date added" value
        row = chapter.find_all('td')

        chapter_name = row[0].text.split(':')[1][1::]
        chapter_href = row[0].find('a')['href']
        chapter_date = row[1].text

        chapter_data = chapter_name, chapter_href, chapter_date
        chapters_array.append(chapter_data)

    return chapters_array


# TODO add function to save in database for further usage of data
# print(grab_all_series())
print(get_all_chapters('/bleach'))
