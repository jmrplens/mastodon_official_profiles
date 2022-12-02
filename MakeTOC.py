
import md_toc

def maketoc(str_readme,lang=""):
    # Find the line where to insert the toc
    line = 0
    found = False
    for linex in str_readme.splitlines():
        if "<!--TOC-->" in linex:
            found = True
            str_readme.split()
            break
        line = line + 1
    if not found: line = 0

    # Find char index to insert TOC
    index = str_readme.index("<!--TOC-->")

    # Create TOC after 'line'
    toc = md_toc.build_toc("README_" + lang + ".md",skip_lines=line,keep_header_levels=5)

    # Remove TOC tag
    str_readme = str_readme.replace("<!--TOC-->", "")

    # Insert TOC
    str_readme = str_readme[:index] + toc + str_readme[index:]

    return str_readme