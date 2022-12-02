
def maketopheader(lang=""):
    # Store TOP header
    if lang == "":
        filepath = '.resources/TOP_HEADER_README_EN.md'
    else:
        filepath = '.resources/TOP_HEADER_README_' + lang + '.md'

    with open(filepath, 'r') as file:
        top_header_text = file.read()
    str_readme = top_header_text + "\n\n"
    return str_readme

def makeheader(lang=""):
    # Store Header
    if lang == "":
        filepath = '.resources/HEADER_README_EN.md'
    else:
        filepath = '.resources/HEADER_README_' + lang + '.md'

    with open(filepath, 'r') as file:
        header_text = file.read()
    str_readme = header_text + "\n<!--TOC-->\n\n" #  "\n<!--ts-->\n<!--te-->" + "\n\n"
    return str_readme

def makefooter(lang=""):
    # Store Footer
    if lang == "":
        filepath = '.resources/FOOTER_README_EN.md'
    else:
        filepath = '.resources/FOOTER_README_' + lang + '.md'

    with open(filepath, 'r') as file:
        footer_text = file.read()
    str_readme = footer_text + "\n\n---"
    return str_readme

def makebottomfooter(lang=""):
    # Store Bottom Footer
    if lang == "":
        filepath = '.resources/BOTTOM_FOOTER_README_EN.md'
    else:
        filepath = '.resources/BOTTOM_FOOTER_README_' + lang + '.md'

    with open(filepath, 'r') as file:
        bottom_footer_text = file.read()
    str_readme = bottom_footer_text
    return str_readme

def makemainbody():
    # Store Body for main README.md
    filepath = '.resources/BODY_README.md'
    with open(filepath, 'r') as file:
        body_text = file.read()
    str_readme = body_text
    return str_readme