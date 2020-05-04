from defines import *
from functions.misc import check_os_for_kindlegen
import subprocess


def generate_mobi(series_name, series_chapter):

    kindlegen_absolute_path = PROJECT_DIR + '/assets/libs/./' + check_os_for_kindlegen()
    html_absolute_path = TEMP_DIR + '/html/' + series_name + '_' + str(series_chapter) + '.html'
    output = str()

    # TODO add output treatment to check which warnings are given
    try:
        output = subprocess.check_output([kindlegen_absolute_path, html_absolute_path]).decode()
    except subprocess.CalledProcessError as error:
        output = error.output.decode()

    print(output)

    return True
