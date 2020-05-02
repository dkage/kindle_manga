import functions.spider as spider
import functions.functions as functions
# import functions.download_chapter as download_chapter
import functions.html_generator as html_generator

print(spider.get_all_series())
# print(spider.get_all_chapters('/naruto'))

# https://www.mangareader.net/bleach/34
# print(spider.get_chapter_size('/bleach/34'))

series = 'one-piece'
chapter = 820
# html_generator.html_gen(series, chapter)
