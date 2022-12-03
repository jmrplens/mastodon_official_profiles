""" Generate MAIN.CSV and README's """

import os
import makemaincsv as Mcsv
import makereadmeheaderfooter as MakeHF
import makemarkdowntables as MakeMD
import maketoc

# Settings
lang_list = ["ES", "EN"]  # Available: "ES", "EN"
ORDER_DATA_BY = "Country"  # Available: "Country"

# First, Append CSV's
Mcsv.makecsv()

# Create README_XX Lists
for lang in lang_list:

    # Make Header For README_XX.md
    topheader = MakeHF.maketopheader(lang)
    header = MakeHF.makeheader(lang)

    # Make Markdown Tables with headings
    mdtables = MakeMD.generate(ORDER_DATA_BY,lang)

    # Make Footer For README_XX.md
    footer = MakeHF.makefooter(lang)
    bottomfooter = MakeHF.makebottomfooter(lang)

    # Concatenate strings
    str_readme = topheader + header + mdtables + footer + bottomfooter

    # Create file if no exist
    if not os.path.exists("README_" + lang + ".md"):
        with open("README_" + lang + ".md", 'w',encoding="utf-8"):
            pass

    # Create TOC
    str_readme = maketoc.maketoc(str_readme,lang)

    # Write .md file
    text_file = open("README_" + lang + ".md", "wt", encoding="utf-8")
    text_file.write(str_readme)
    text_file.close()

# Create Main README.md

# Make Header For README.md
topheader = MakeHF.maketopheader()

# Make Body For README.md
body = MakeHF.makemainbody()

# Make Footer For README.md
footer = MakeHF.makefooter()
bottomfooter = MakeHF.makebottomfooter()

# Concatenate strings
str_readme = topheader + body + footer + bottomfooter

# Write .md file
text_file = open("README.md", "wt", encoding="utf-8")
text_file.write(str_readme)
text_file.close()
