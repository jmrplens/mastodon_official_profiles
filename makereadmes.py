"""
Library
"""
import md_toc
import pandas as pd  # To import CSV and Markdown conversion
import numpy as np
import glob
import os
import yaml
from types import SimpleNamespace
from bs4 import BeautifulSoup

#  from deep_translator import GoogleTranslator  # To translate Country names and table column names

# Public methods
__all__ = ['makecsv', 'create_localised_readme', 'create_main_readme', 'update_svg']


def makecsv():
    """Make MAIN.csv"""
    # Get all CSV Filepaths - Ignore 'docs' folder
    result = list(set(glob.glob("*/**.csv")) - set(glob.glob("docs/**", recursive=True)))

    # Loop over files to create dictionary (Key=filepath, Value=markdown table)
    df_append = pd.DataFrame()  # To main.csv file
    for file in result:
        DF = pd.read_csv(file)
        DF.fillna("-", inplace=True)  # Fill empty cells with "-"
        # Sort Rows by name account
        DF.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
        DF.to_csv(file, index=False)  # Update CSV file
        # Append CSV data to create MAIN.CSV
        DF['FILEPATH'] = file
        filename = os.path.basename(file).split('/')[-1]
        DF['FILENAME'] = filename[0:len(filename) - 4]  # Remove ".csv"
        df_append = pd.concat([df_append, DF], ignore_index=True)

    # Save MAIN.csv
    df_append.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
    df_append.to_csv("MAIN.csv", index=False)

    # Save MAIN.csv without irrelevant columns
    df_web = df_append.iloc[:, 0:11]
    df_web.to_csv("docs/MAIN_web.csv", index=False)

    return df_append


def create_localised_readme(lang_list, order_by, df) -> None:
    # Create README_XX Lists
    for lang in lang_list:
        # Make Header For README_XX.md
        topheader = _maketopheader(lang)
        header = _makeheader(lang)

        # Make Markdown Tables with headings
        mdtables = _generate(order_by, lang, df)

        # Make Footer For README_XX.md
        footer = _makefooter(lang)
        bottomfooter = _makebottomfooter(lang)

        # Concatenate strings
        str_readme = topheader + header + mdtables + footer + bottomfooter

        # Create TOC
        str_readme = _maketoc(str_readme, lang)

        # Write .md file
        _writefile("README_" + lang + ".md", str_readme)


def create_main_readme() -> None:
    # Make Header For README.md
    topheader = _maketopheader()

    # Make Body For README.md
    body = _makemainbody()

    # Make Footer For README.md
    footer = _makefooter()
    bottomfooter = _makebottomfooter()

    # Concatenate strings
    str_readme = topheader + body + footer + bottomfooter

    # Write .md file
    _writefile("README.md", str_readme)


def _writefile(filepath, content) -> None:
    text_file = open(filepath, _openmethod(), encoding=_encoding())
    text_file.write(content)
    text_file.close()


def _readfile(filepath):
    with open(filepath, 'r', encoding=_encoding()) as file:
        text = file.read()
    return text


def _maketopheader(lang=""):
    """Create TOP header"""
    if lang == "":
        filepath = '.resources/TOP_HEADER_README_EN.md'
    else:
        filepath = '.resources/TOP_HEADER_README_' + lang + '.md'
    text = _readfile(filepath)
    str_readme = text + "\n\n"
    return str_readme


def _makeheader(lang=""):
    """Create header"""
    if lang == "":
        filepath = '.resources/HEADER_README_EN.md'
    else:
        filepath = '.resources/HEADER_README_' + lang + '.md'
    text = _readfile(filepath)
    str_readme = text + "\n<!--TOC-->\n\n"
    return str_readme


def _makefooter(lang=""):
    """Create footer"""
    if lang == "":
        filepath = '.resources/FOOTER_README_EN.md'
    else:
        filepath = '.resources/FOOTER_README_' + lang + '.md'
    text = _readfile(filepath)
    if lang.lower() == "en":
        str_readme = "## Contributors\n\n <!--CONTRIBUTORS-->\n\n" + text + "\n\n---"
    elif lang.lower() == "es":
        str_readme = "## Colaboradorxs\n\n <!--CONTRIBUTORS-->\n\n" + text + "\n\n---"
    else:
        str_readme = "## Contributors\n\n <!--CONTRIBUTORS-->\n\n" + text + "\n\n---"
    str_readme = _makecontributors(str_readme)
    return str_readme


def _makebottomfooter(lang=""):
    """Create bottom footer"""
    if lang == "":
        filepath = '.resources/BOTTOM_FOOTER_README_EN.md'
    else:
        filepath = '.resources/BOTTOM_FOOTER_README_' + lang + '.md'
    text = _readfile(filepath)
    str_readme = text
    return str_readme


def _makemainbody():
    """Create body for main README"""
    filepath = '.resources/BODY_README.md'
    text = _readfile(filepath)
    str_readme = text
    return str_readme


def _maketoc(str_readme, lang=""):
    """Find the line where to insert the toc"""
    line = 0
    found = False
    for linex in str_readme.splitlines():
        if "<!--TOC-->" in linex:
            found = True
            str_readme.split()
            break
        line = line + 1
    if not found:
        line = 0

    # Find char index to insert TOC
    index = str_readme.index("<!--TOC-->")

    # Create TOC after 'line'
    toc = md_toc.build_toc("README_" + lang + ".md", skip_lines=line, keep_header_levels=5)

    # Remove TOC tag
    str_readme = str_readme.replace("<!--TOC-->", "")

    # Insert TOC
    str_readme = str_readme[:index] + toc + "<br />" + str_readme[index:]

    return str_readme

def _makecontributors(str_readme):
    """Find the line where to insert the contributors"""
    line = 0
    found = False
    for linex in str_readme.splitlines():
        if "<!--TOC-->" in linex:
            found = True
            str_readme.split()
            break
        line = line + 1
    if not found:
        line = 0

    # Find char index to insert TOC
    index = str_readme.index("<!--CONTRIBUTORS-->")

    # Create TOC after 'line'
    contri_text = _contributors_table("CONTRIBUTORS.yml", cols=2, link_cols=3)

    # Remove TOC tag
    str_readme = str_readme.replace("<!--CONTRIBUTORS-->", "")

    # Insert TOC
    str_readme = str_readme[:index] + contri_text + "<br />" + str_readme[index:]

    return str_readme


def _openmethod():
    """ Open file method """
    return 'w+'


def _encoding():
    """ File encoding """
    return "utf-8"


def update_svg(lang, df) -> None:
    # Update SVG DATABASE TOTAL PROFILES
    filename = ".resources/information/DATABASE_PROFILES_NUM_" + lang + ".svg"
    filenametemp = ".resources/information/DATABASE_PROFILES_NUM_TMP_" + lang + ".svg"
    open(filename, _openmethod(), encoding=_encoding()) \
        .write(open(filenametemp, encoding=_encoding()) \
               .read().replace('XXXX', str(len(df))))


def _gen_by_country(lang, df, str_readme=""):
    """
    Make Markdown Tables. Sorted By Country->Categories->Name
    :param lang:
    :return:
    Nothing
    """

    df_gen = df
    # Update SVG DATABASE TOTAL PROFILES
    update_svg(lang, df)

    # # Translate countries
    # df_gen['Country'] = df_gen['Country'].apply(
    #     lambda x: GoogleTranslator(source = 'auto',
    #                                target = lang.lower()).translate(x).title())
    # # Translate languages
    # df_gen['Language'] = df_gen['Language'].apply(
    #         lambda x: GoogleTranslator(source = 'auto',
    #                                    target = lang.lower()).translate(x).title())

    # Sort by country
    df_gen.sort_values(by='Country', inplace=True,
                       key=lambda col: col.str.lower())
    # Get country list
    country_list = df_gen["Country"].unique()
    # For each country
    for country in country_list:
        # Print Country heading
        icon_country = '<img align="left" height="35"' \
                       + ' src=".resources/icons/country.svg#gh-light-mode-only"' \
                       + ' alt="Country">' \
                       + '<img align="left" height="35"' \
                       + ' src=".resources/icons/country_dark.svg#gh-dark-mode-only"' \
                       + ' alt="Country">'
        str_readme = str_readme \
                     + icon_country \
                     + "\n\n## " \
                     + country \
                     + '\n\n<img align="left" height="10"' \
                     + ' src=".resources/icons/sep.svg" alt="Separator"><br>\n\n'
        #
        profiles_country = df_gen.loc[df_gen["Country"] == country]
        df_cp = profiles_country.copy()  # To avoid "SettingWithCopyWarning"
        df_cp.sort_values(by='Country', inplace=True, key=lambda col: col.str.lower())
        profiles_country = df_cp

        # Get category list
        category_list = profiles_country["CATEGORY_" + lang].unique()
        category_list = np.sort(category_list)  # Sort categories
        # For each category
        for category in category_list:
            # print(category)
            data = df_gen.loc[ \
                (df_gen['Country'] == country) & (df_gen["CATEGORY_" + lang] == category) \
                ]
            # Sort by name
            df_cp = data.copy()  # To avoid "SettingWithCopyWarning"
            df_cp.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
            data = df_cp

            # Print Category heading
            icon_category = \
                '<img align="left" height="30" src=".resources/icons/' \
                + data['FILENAME'].values[0] + '.svg" alt="Country">'
            str_readme = str_readme \
                         + icon_category \
                         + "\n\n### " \
                         + category \
                         + '\n\n<img align="left" height="5" \
                                src=".resources/icons/subsep.svg" alt="Separator">\n\n'
            # Markdown
            md_table = data.iloc[:, 0:9].to_markdown(index=False)
            # Print Table
            str_readme = str_readme + md_table + "\n\n"
            badge = \
                "[![View CSV]" \
                + "(https://img.shields.io/badge/" \
                + "CSV-View%20data%20in%20CSV%20file-brightgreen)](" \
                + data.iloc[0]["FILEPATH"] \
                + ")"
            str_readme = str_readme + badge + '\n\n'
        str_readme = str_readme + "---\n<br>\n\n"
    return str_readme


def _generate(orderby, lang, df):
    orderby = orderby.lower()
    if orderby == "country":
        str_readme = _gen_by_country(lang, df)
    else:
        str_readme = "Not generated"
    return str_readme


def _contributors_table(filepath,cols=2,link_cols=3):
    # Settings
    datafile = _readfile(filepath)
    # cols = 2  # Contributors table columns
    # link_cols = 3  # Links button columns

    # Parse YAML data
    data_list = yaml.load(datafile, Loader=yaml.Loader)

    # Initialize html table
    table_html_str = '<table>\n<tbody>\n<tr>\n'

    # Load contributor information and append to html table
    str_temp = ''
    for index, contributor in enumerate(data_list):

        if index % cols == 0 and index > 0:  # New column
            table_html_str = table_html_str + '</tr>\n<tr>\n'

        n = SimpleNamespace(**contributor)  # Store data in 'n'

        # Has a name
        if hasattr(n, 'name'):
            if not n.name:  # Check if not empty
                name = False
            else:
                name = n.name
        else:
            name = False
        # Has GitHub user
        if hasattr(n, 'github_user'):
            if not n.github_user:  # Check if not empty
                github_user = False
            else:
                github_user = n.github_user
        else:
            github_user = False
        # Has avatar
        if hasattr(n, 'avatar'):
            if not n.avatar:  # Check if not empty
                avatar = False
            else:
                avatar = n.avatar
        else:
            avatar = False
        # Link for avatar and name
        if isinstance(github_user, str):
            name_link = "https://github.com/" + github_user
        elif "web" in n.links:
            name_link = n.links["web"]
        else:
            name_link = False

        # Avatar and name
        str_temp = '<td width="140px" align="center">\n' \
                   + '{link}'.format(link='<a href="' + name_link + '">\n' if name_link else '') \
                   + '{image}'.format(
            image='<img src="' + avatar + '" width="100px;"/>\n' if isinstance(avatar, str) else '') \
                   + '{name_text}'.format(
            name_text='<p><sub><b>' + name + '</b></sub></p>\n' if isinstance(name, str) else '') \
                   + '{link}'.format(link='</a>\n' if name_link else '')
        table_html_str = table_html_str + str_temp

        # Links
        str_temp = ''
        idx = 0
        for type_link, link in n.links.items():
            if idx % link_cols == 0 and idx > 0:  # New line
                str_temp = str_temp + '<br />\n'
            if isinstance(link, list):  # If 'link' have more than 1 link, iterate
                for single_link in link:
                    idx = idx + 1
                    str_temp = str_temp + '<a href="' + single_link + '" title="' + type_link + '">\n' \
                               + '<img src=".resources/icons/' + type_link + '.svg" height="22"/></a>\n'
            else:
                idx = idx + 1
                str_temp = str_temp + '<a href="' + link + '" title="' + type_link + '">\n' \
                           + '<img src=".resources/icons/' + type_link + '.svg" height="22"/></a>\n'

        # Link to commits if github_user else 'external'
        if isinstance(github_user, str):
            str_temp = str_temp \
                       + '<br />\n' \
                       + '<a href = "https://github.com/jmrplens/mastodon_official_profiles/commits?' \
                       + 'author=' + github_user + '"' \
                       + 'title = "COMMITS">\n<img src=".resources/buttons/COMMITS.svg" height="25" width="85px"/></a>\n'
        else:
            str_temp = str_temp \
                       + '<br />\n' \
                       + '{link}'.format(link='<a href="' + name_link + '" title="EXTERNAL">\n' if name_link else '') \
                       + '<img src=".resources/buttons/EXTERNAL.svg" height="25" width="85px"/>\n' \
                       + '{link}'.format(link='</a>\n' if name_link else '')

        table_html_str = table_html_str + str_temp + '</td>\n'

    table_html_str = table_html_str + '</tr>\n</tbody>\n</table>'

    pretty_html = BeautifulSoup(table_html_str, features="lxml").prettify()

    return pretty_html
