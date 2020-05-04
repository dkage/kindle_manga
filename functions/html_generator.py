from functions.misc import *
from natsort import natsorted
import sys
import os


# To guarantee usage of CSS, it's better to insert it into an style tag.
def grab_css():
    # TODO CSS needs rework to improve image to screen size ratio (too many blank spaces around image)
    #  more trial and error needed
    with open('../css/manga_gen.css', 'r') as css_file:
        css_properties = css_file.read().replace('\n', '')
        style_tag = "<style> " + css_properties + " </style>"

        return style_tag


def html_gen(series_name, chapter_number):

    # Grab list of image files to put into HTML
    images_list = sorted(os.listdir(get_chapter_full_path(series_name, chapter_number)))
    # Natural sort images to have "1, 2, 3... 10, 12" instead of "1, 10, 11, 2, 3..." you get by using normal sorted()
    sorted_images_list = natsorted(images_list, key=lambda y: y.lower())

    # GENERATES HTML to then transform into mobi type
    doctype = "<!DOCTYPE html>" \
              "     <html>"
    head_and_css = "<head>" + grab_css() + "</head>"
    body_start = "<body>"

    content = "<div id='imgs_container'>"

    chapter_relative_path = '../' + series_name + '/' + str(chapter_number) + '/' # This path is relative to HTML
    print(chapter_relative_path)

    for image in sorted_images_list:
        img_element = "<img src='" + chapter_relative_path + image + "'>"
        content = content + img_element
    content = content + "</div>"
    body_end = "</body></html>"

    # Concatenates every variable needed to create html
    html_to_save = doctype + head_and_css + body_start + content + body_end

    # Create dir if doesn't exist
    tmp_dir = '../tmp/html/'
    check_dir(tmp_dir)

    # Save to file
    html_file = open(tmp_dir + series_name + '_' + str(chapter_number) + '.html', 'w')
    html_file.write(html_to_save)
    html_file.close()
    print('HTML file generated for:  ' + series_name + '_' + str(chapter_number))

    return True
