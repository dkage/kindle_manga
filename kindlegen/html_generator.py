import os
from functions import get_full_path, check_dir

# GENERATES HTML
# TODO this needs to be changed into functions or class
doctype = "<!DOCTYPE html>" \
          "     <html>"
# TODO CSS needs rework to improve image to screen size ratio (too many blank spaces) more trial and error needed
head_and_css = "<head>" \
               "    <link rel='stylesheet' href='../../css/manga.css'>" \
               "</head>"
body_start = "<body>"

content = "<div id='imgs_container'>"

# TODO refactor these variables (maybe a def?)
series = 'one-piece'
chapter_images = sorted(os.listdir(get_full_path('one-piece', 813)))
for image in chapter_images:
    img_element = "<img src='../../" + get_full_path('one-piece', 813) + '/' + image + "'>"
    content = content + img_element
content = content + "</div>"
body_end = "</body></html>"


html_to_save = doctype + head_and_css + body_start + content + body_end
dir = './tmp/html/'
check_dir(dir)
html_file = open(dir + 'tmp.html', 'w')
html_file.write(html_to_save)
html_file.close()

