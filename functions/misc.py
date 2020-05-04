import os
from defines import *
from platform import system


def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_chapter_full_path(series_name, series_chapter):
    return TEMP_DIR + '/' + series_name + '/' + str(series_chapter)


def check_os_for_kindlegen():
    current_os = system()
    if current_os == 'Darwin':
        return 'kindlegen_64_macos'
    elif current_os == 'Win32':
        return ' '  # TODO download kindlegen for Windows
    else:
        return 'kindlegen_32_linux'
