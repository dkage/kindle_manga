from bs4 import BeautifulSoup
import requests
import shutil
from functions import functions
from defines import *
import sys


# Spider functions designed to crawl only mangareader (maybe add more sources later [maybe scanlators])



def get_all_series():
    """
    Gets all series names that are available on mangareader.net

    :return: A list of tuples, where each one contains two values:  ( <series_name>, <url>
    """

    print('Grabbing series available on mangareader.net')
    alphabetic_list = '/alphabetical'

    try:
        http_return = requests.get(BASE_URL + alphabetic_list)
    except requests.exceptions.ConnectionError:
        print('BAD HTTP request response. Is connection online?' + str())
        return 'Error 001.1'

    print('GOOD HTTP request response. Code: ' + str(http_return.status_code))

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

    :param series_link:  parameter as '/series' path to add to BASE_URL
    :return: returns array with a three items tuple containing in this exact order:
                chapter_name, chapter_path, date_chapter_was_added
    """

    chapters_array = []
    series_url = BASE_URL + series_link

    # TODO add requests error handling for bad conn
    http_return = requests.get(series_url)
    soup = BeautifulSoup(http_return.content, 'lxml')
    series_chapters = soup.find('table', {'id': 'listing'}).find_all('tr')

    # Skip first row using 1:: to ignore column headers
    for chapter in series_chapters[1::]:

        # Each row has two TDs, first one contains href and chapter name, second has "date added" value
        row = chapter.find_all('td')

        chapter_number = row[0].text.split(': ', 1)[0].split(' ', 1)[1].strip()
        chapter_name = row[0].text.split(':', 1)[1].strip()
        chapter_href = row[0].find('a')['href']
        chapter_date = row[1].text

        chapter_data = chapter_number, chapter_name, chapter_href, chapter_date
        chapters_array.append(chapter_data)

    return chapters_array


def get_chapter_size(series_name, series_chapter):
    """
    :param series_name: name of the series in url.
    :param series_chapter: receives chapter number to check size.
    :return: number of pages for that particular chapter
    """

    # TODO add requests error handling for bad conn 2
    http_return = requests.get(BASE_URL + '/' + series_name + '/' + str(series_chapter))

    soup = BeautifulSoup(http_return.content, 'lxml')
    pages_number = soup.find('div', {'id': 'selectpage'}).text.split('of')[1].strip()

    return pages_number


def download_chapter(series_name, series_chapter):

    manga_full_path = TEMP_DIR + '/' + series_name + '/' + str(series_chapter) + '/'
    full_url = BASE_URL + '/' + series_name + '/' + str(series_chapter)

    # Check if directories exist, if false, they are created.
    functions.check_dir(TEMP_DIR)
    functions.check_dir(TEMP_DIR + '/' + series_name)
    functions.check_dir(manga_full_path)

    # Check number of pages chapter has, each will be requested individually
    last_page = get_chapter_size(series_name, series_chapter)
    print('This ' + series_name + ' chapter has ' + str(last_page) + ' pages')

    for page in range(1, int(last_page) + 1):
        print('Downloading -' + series_name + ' chapter ' + str(series_chapter) + ' - PAGE ' + str(page))
        http_return = requests.get(full_url + '/' + str(page))
        soup = BeautifulSoup(http_return.content, 'lxml')
        img_div = soup.find("div", {"id": "imgholder"}).find("img")['src']

        img_request = requests.get(img_div, stream=True)
        with open(manga_full_path + str(page) + '.jpg', 'wb') as out_file:
            shutil.copyfileobj(img_request.raw, out_file)

    print('Chapter downloaded successfully.')

    return 'Done'
