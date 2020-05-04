import sys
import functions.spider as spider
import functions.functions as functions
import functions.html_generator as html_generator



# print(spider.get_all_series())
# print(spider.get_all_chapters('/naruto'))

# https://www.mangareader.net/bleach/34
# print(spider.get_chapter_size('/naruto/382'))


spider.download_chapter('naruto', '382')


# series = 'naruto'
# chapter = '500'
# html_generator.html_gen(series, chapter)
