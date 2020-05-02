import os


# TODO is this useful?

def check_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_full_path(series, chapter):
    main_path = './tmp/'
    series_dir = series + '/'

    return main_path + series_dir + str(chapter)
