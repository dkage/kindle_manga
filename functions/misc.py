import os
from defines import *


def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_chapter_full_path(series_name, series_chapter):
    return TEMP_DIR + '/' + series_name + '/' + str(series_chapter)
