import os


# TODO is this useful?

def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_full_path(series, chapter):
    main_path = './tmp/'
    series_dir = series + '/'

    return main_path + series_dir + str(chapter)
