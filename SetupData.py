
import os

import MakeReadmeHeaderAndFooter as MakeHF
import MakeMarkdownTables as MakeMD
import MakeTOC

# Settings
lang_list = ["ES", "EN"]  # Available: "ES", "EN"
order_data_by = "Country"  # Available: "Country"

# First, Append CSV's
exec(open("./MakeMainCSV.py").read())

# Create README_XX Lists
for idx in range(len(lang_list)):

    # Make Header For README_XX.md
    topheader = MakeHF.maketopheader(lang_list[idx])
    header = MakeHF.makeheader(lang_list[idx])

    # Make Markdown Tables with headings
    mdtables = MakeMD.generate(order_data_by,lang_list[idx])

    # Make Footer For README_XX.md
    footer = MakeHF.makefooter(lang_list[idx])
    bottomfooter = MakeHF.makebottomfooter(lang_list[idx])

    # Concatenate strings
    str_readme = topheader + header + mdtables + footer + bottomfooter

    # Create file if no exist
    if not os.path.exists("README_" + lang_list[idx] + ".md"):
        with open("README_" + lang_list[idx] + ".md", 'w'): pass

    # Create TOC
    str_readme = MakeTOC.maketoc(str_readme,lang_list[idx])

    # Write .md file
    text_file = open("README_" + lang_list[idx] + ".md", "wt")
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
text_file = open("README.md", "wt")
text_file.write(str_readme)
text_file.close()