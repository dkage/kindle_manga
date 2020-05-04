import os
from defines import *
from functions.misc import check_os_for_kindlegen
from shlex import quote as shlex_quote


def generate_mobi(series_name, series_chapter):
    # TODO change this for subprocess module to capture cli response

    html_absolute_path = TEMP_DIR + '/html/' + series_name + '_' + str(series_chapter) + '.html'
    kindlegen_absolute_path = PROJECT_DIR + '/assets/libs/./' + check_os_for_kindlegen()

    os.system(shlex_quote(kindlegen_absolute_path + ' ' + html_absolute_path))

    return True
