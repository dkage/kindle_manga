import sys
import functions.spider as spider
import functions.misc as misc
import functions.html_generator as html_generator
import functions.kindlegen_handler as kindle
from defines import *
import os


series = 'naruto'
chapter = '382'

# print(spider.get_all_series())
# print(spider.get_all_chapters('/naruto'))

# https://www.mangareader.net/bleach/34
# print(spider.get_chapter_size('/naruto/382'))


# spider.download_chapter('naruto', '382')
#


# html_generator.html_gen(series, chapter)

# print(html_generator.grab_css())

# series_name = 'naruto'
# chapter_number = 382

# print(PROJECT_DIR)
# print(os.listdir(misc.get_chapter_full_path(series_name, chapter_number)))

# html_generator.html_gen(series_name, chapter_number)
kindle.generate_mobi(series, chapter)

