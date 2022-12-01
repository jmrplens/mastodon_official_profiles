# README CREATOR
# Jose M. Requena Plens

import pandas as pd  # To import CSV and Markdown conversion
import numpy as np
#  from deep_translator import GoogleTranslator  # To translate Country names and table column names

# First, Append CSV's
import AppendCSV
AppendCSV


df = pd.read_csv("MAIN.csv")
order_data_by = "Country"  # Available: "Country"


def gen_by_country(lang):
    # print(lang)
    # Store top header
    with open('.resources/TOP_HEADER_README_' + lang + '.md', 'r') as file:
        top_header_text = file.read()
    str_readme = top_header_text + "\n\n"
    # Store header
    with open('.resources/HEADER_README_' + lang + '.md', 'r') as file:
        header_text = file.read()
    str_readme = str_readme + header_text + "\n<!--ts-->\n<!--te-->" + "\n\n"
    df_gen = df
    # # Translate countries
    # df_gen['Country'] = df_gen['Country'].apply(
    #     lambda x: GoogleTranslator(source = 'auto',
    #                                target = lang.lower()).translate(x).title())
    # # Translate languages
    # df_gen['Language'] = df_gen['Language'].apply(
    #         lambda x: GoogleTranslator(source = 'auto',
    #                                    target = lang.lower()).translate(x).title())

    # Sort by country
    df_gen.sort_values( by = 'Country', inplace = True,
                       key = lambda col: col.str.lower() )
    # Get country list
    country_list = df_gen["Country"].unique()
    # For each country
    for country in country_list:
        # Print Country heading
        icon_country = '<img align="left" height="50" src=".resources/icons/country.svg#gh-light-mode-only" alt="Country"><img align="left" height="35" src=".resources/icons/country_dark.svg#gh-dark-mode-only" alt="Country">'
        str_readme = str_readme + icon_country + "\n\n## " + country + '\n\n<img align="left" height="10" src=".resources/icons/sep.svg" alt="Separator"><br>\n\n'
        #
        profiles_country = df_gen.loc[df_gen["Country"] == country]
        profiles_country.sort_values(by = 'Country', inplace = True,
                                     key = lambda col: col.str.lower())
        # print(country)
        # Get category list
        category_list = profiles_country["CATEGORY_"+lang].unique()
        category_list = np.sort(category_list)  # Sort categories
        # For each category
        for category in category_list:
            # print(category)
            data = df_gen.loc[(df_gen['Country'] == country) & (df_gen["CATEGORY_"+lang] == category)]
            # Sort by name
            data.sort_values(by = 'Name', inplace = True,
                             key = lambda col: col.str.lower())
            # print(data)
            # Print Category heading
            icon_category = '<img align="left" height="30" src=".resources/icons/' + data['FILENAME'].values[0] + '.svg" alt="Country">'
            str_readme = str_readme + icon_category + "\n\n### " + category + '\n\n<img align="left" height="5" src=".resources/icons/subsep.svg" alt="Separator">\n\n'
            # Markdown
            md_table = data.iloc[:, 0:9].to_markdown(index = False)
            # Print Table
            str_readme = str_readme + md_table + "\n\n"
            badge = "[![View CSV](https://img.shields.io/badge/CSV-View%20data%20in%20CSV%20file-brightgreen)](" + data.iloc[0]["FILEPATH"] + ")"
            str_readme = str_readme + badge + '\n\n'
        str_readme = str_readme + "---\n<br>\n\n"
    # Store Footer
    with open('.resources/FOOTER_README_' + lang + '.md', 'r') as file:
        footer_text = file.read()
    str_readme = str_readme + footer_text  + "\n\n---"
    # Store Bottom Footer
    with open( '.resources/BOTTOM_FOOTER_README_' + lang + '.md', 'r' ) as file:
        bottom_footer_text = file.read()
    str_readme = str_readme + bottom_footer_text
    # Write .md file
    text_file = open("README_" + lang + ".md", "wt")
    text_file.write(str_readme)
    text_file.close()


def generate(orderby, lang):
    func = "gen_by_" + orderby.lower()
    eval(func + '("' + lang + '")')
    return


lang_list = ["ES", "EN"]
for idx in range(len(lang_list)):
    generate(order_data_by, lang_list[idx])
