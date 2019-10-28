import os
from functions import get_full_path, check_dir


def html_gen(series_name, chapter_number):
    # GENERATES HTML to then transform into mobi type
    # TODO this needs to be changed into functions or class
    doctype = "<!DOCTYPE html>" \
              "     <html>"
    # TODO CSS needs rework to improve image to screen size ratio (too many blank spaces around image)
    #  more trial and error needed
    head_and_css = "<head>" \
                   "    <link rel='stylesheet' href='../../css/manga_html.css'>" \
                   "</head>"
    body_start = "<body>"

    content = "<div id='imgs_container'>"
    chapter_images = sorted(os.listdir(get_full_path(series_name, chapter_number)))
    for image in chapter_images:
        img_element = "<img src='../../" + get_full_path(series_name, chapter_number) + '/' + image + "'>"
        content = content + img_element
    content = content + "</div>"
    body_end = "</body></html>"

    # Concatenates every variable needed to create html
    html_to_save = doctype + head_and_css + body_start + content + body_end
    tmp_dir = './tmp/html/'
    check_dir(tmp_dir)
    html_file = open(tmp_dir + series + '-' + str(chapter) + '.html', 'w')
    html_file.write(html_to_save)
    html_file.close()

    return True


series = 'one-piece'
chapter = 820
html_gen(series, chapter)
