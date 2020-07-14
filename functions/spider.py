import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup
from functions.misc import *
from defines import *
from time import sleep
from defines import COVERS_DIR


# Spider scraper functions designed to crawl only mangareader (maybe add more sources later [maybe scanlators])
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
    series_cards = soup.find_all('div', {"class": "d40"})

    series_array = []
    for column in series_cards:
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
    try:
        series_chapters = soup.find('table', {'class': 'd48'}).find_all('tr')
    except BeautifulSoup.AttributeError:
        return 'Error. Soup problem'

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

    # chapters_qnt = len(chapters_array) + 1
    # return chapters_array, chapters_qnt

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
    # TODO add docs
    manga_full_path = get_chapter_full_path(series_name, series_chapter)
    full_url = BASE_URL + '/' + series_name + '/' + str(series_chapter)

    # Check if directories exist, if false, they are created.
    check_dir(TEMP_DIR)
    check_dir(TEMP_DIR + '/' + series_name)
    check_dir(manga_full_path)

    # Check number of pages chapter has, each will be requested individually
    last_page = get_chapter_size(series_name, series_chapter)
    print('This ' + series_name + ' chapter has ' + str(last_page) + ' pages')

    for page in range(1, int(last_page) + 1):
        print('Downloading - ' + series_name.upper() + ' chapter ' + str(series_chapter) + ' - PAGE ' + str(page))

        http_return = requests.get(full_url + '/' + str(page))
        soup = BeautifulSoup(http_return.content, 'lxml')
        img_div = soup.find("div", {"id": "imgholder"}).find("img")['src']

        img_request = requests.get(img_div, stream=True)
        with open(manga_full_path + '/' + str(page) + '.jpg', 'wb') as out_file:
            shutil.copyfileobj(img_request.raw, out_file)
        sleep(3)

    print('Chapter downloaded successfully.')

    return True


def get_image_url(series_url):
    # TODO add docs
    
    try:
        http_return = requests.get(BASE_URL + series_url)
        print(http_return)
    except requests.exceptions.ConnectionError:
        print('BAD HTTP request response. Is connection online?' + str())
        return 'Error code: IM001'

    soup = BeautifulSoup(http_return.content, 'lxml')
    img_src = soup.find('div', {'class': 'd38'}).find('img')['src']

    return img_src


def download_cover(series_url):
    # TODO add docs

    image_url = get_image_url(series_url)

    http_return = requests.get(image_url, stream=True)
    img_name = ''.join([series_url.replace('/', ''), '.jpg'])

    if http_return.status_code == 200:
        http_return.raw.decode_content = True

        with open(os.path.join(COVERS_DIR, img_name), 'wb') as f:
            shutil.copyfileobj(http_return.raw, f)

        del http_return

    return 'Success'
