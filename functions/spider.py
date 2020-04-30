from bs4 import BeautifulSoup
import requests

# Spider functions designed to crawl only mangareader (maybe add more sources later [maybe scanlators])
base_url = 'https://www.mangareader.net'


def get_all_series():
    """
    Gets all series names that are available on mangareader.net

    :return: A list of tuples, where each one contains two values:  ( <series_name>, <url>
    """

    alphabetic_list = '/alphabetical'
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
    """
    Function to grab all the chapters from a series

    :param series_link:  parameter as '/series' path to add to base_url
    :return: returns array with a three items tuple containing in this exact order:
                chapter_name, chapter_path, date_chapter_was_added
    """

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


def get_chapter_size(series_chapter):
    """
    :param series_chapter: receives '/series/1' url suffix.
    :return: number of pages for that particular chapter
    """

    http_return = requests.get(base_url + series_chapter)
    soup = BeautifulSoup(http_return.content, 'lxml')

    pages_number = soup.find('div', {'id': 'selectpage'}).text.split('of ')[1]
    return pages_number


# print(get_all_series())
print(get_all_chapters('/bleach'))

# https://www.mangareader.net/bleach/34
# print(get_chapter_size('/bleach/34'))
