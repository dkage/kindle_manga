doctype = "<!DOCTYPE html><html>"
head_and_css = "<head>" \
               "    <link rel='stylesheet' href='../css/manga.css'>" \
               "</head>"
body_start = "<body>"

# TODO add logic to insert every image in a loop
content = 'IMGS GO HERE'

body_end = "</body></html>"

html_to_save = doctype + head_and_css + body_start + content + body_end
