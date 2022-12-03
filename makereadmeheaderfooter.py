
def maketopheader(lang=""):
    """Create TOP header"""
    if lang == "":
        filepath = '.resources/TOP_HEADER_README_EN.md'
    else:
        filepath = '.resources/TOP_HEADER_README_' + lang + '.md'

    with open(filepath, 'r',encoding="utf-8") as file:
        top_header_text = file.read()
    str_readme = top_header_text + "\n\n"
    return str_readme

def makeheader(lang=""):
    """Create header"""
    if lang == "":
        filepath = '.resources/HEADER_README_EN.md'
    else:
        filepath = '.resources/HEADER_README_' + lang + '.md'

    with open(filepath, 'r',encoding="utf-8") as file:
        header_text = file.read()
    str_readme = header_text + "\n<!--TOC-->\n\n" #  "\n<!--ts-->\n<!--te-->" + "\n\n"
    return str_readme

def makefooter(lang=""):
    """Create footer"""
    if lang == "":
        filepath = '.resources/FOOTER_README_EN.md'
    else:
        filepath = '.resources/FOOTER_README_' + lang + '.md'

    with open(filepath, 'r',encoding="utf-8") as file:
        footer_text = file.read()
    str_readme = footer_text + "\n\n---"
    return str_readme

def makebottomfooter(lang=""):
    """Create bottom footer"""
    if lang == "":
        filepath = '.resources/BOTTOM_FOOTER_README_EN.md'
    else:
        filepath = '.resources/BOTTOM_FOOTER_README_' + lang + '.md'

    with open(filepath, 'r',encoding="utf-8") as file:
        bottom_footer_text = file.read()
    str_readme = bottom_footer_text
    return str_readme

def makemainbody():
    """Create body for main README"""
    filepath = '.resources/BODY_README.md'
    with open(filepath, 'r',encoding="utf-8") as file:
        body_text = file.read()
    str_readme = body_text
    return str_readme