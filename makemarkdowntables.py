""" README CREATOR """
# Jose M. Requena Plens

import pandas as pd  # To import CSV and Markdown conversion
import numpy as np
#  from deep_translator import GoogleTranslator  # To translate Country names and table column names

# Get Database
df = pd.read_csv("MAIN.csv")

def jls_extract_def():
    """ Open file method """
    return 'wt'


def gen_by_country(lang):
    """
    Make Markdown Tables. Sorted By Country->Categories->Name
    :param lang:
    :return:
    Nothing
    """

    str_readme = ""
    df_gen = df
    # Update SVG DATABASE TOTAL PROFILES
    filename = ".resources/information/DATABASE_PROFILES_NUM_" + lang + ".svg"
    filenametemp = ".resources/information/DATABASE_PROFILES_NUM_TMP_" + lang + ".svg"
    open(filename, jls_extract_def(),encoding="utf-8")\
        .write(open(filenametemp,encoding="utf-8")\
            .read().replace('XXXX', str(len(df_gen))))

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
        icon_country = \
            '<img align="left" height="50" \
                src=".resources/icons/country.svg#gh-light-mode-only" \
                alt="Country">\
                    <img align="left" height="35" \
                        src=".resources/icons/country_dark.svg#gh-dark-mode-only" \
                            alt="Country">'
        str_readme = str_readme \
            + icon_country \
                + "\n\n## " \
                    + country \
                        + '\n\n<img align="left" height="10" \
                            src=".resources/icons/sep.svg" alt="Separator"><br>\n\n'
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
            data = df_gen.loc[\
                (df_gen['Country'] == country) & (df_gen["CATEGORY_"+lang] == category)\
                    ]
            # Sort by name
            data.sort_values(by = 'Name', inplace = True,
                             key = lambda col: col.str.lower())
            # print(data)
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
            md_table = data.iloc[:, 0:9].to_markdown(index = False)
            # Print Table
            str_readme = str_readme + md_table + "\n\n"
            badge = \
                "[![View CSV]\
                    (https://img.shields.io/badge/CSV-View%20data%20in%20CSV%20file-brightgreen)\
                        ](" + data.iloc[0]["FILEPATH"] + ")"
            str_readme = str_readme + badge + '\n\n'
        str_readme = str_readme + "---\n<br>\n\n"
    return str_readme


def generate(orderby, lang):
    """ Eval function """
    func = "gen_by_" + orderby.lower()
    str_readme = eval(func + '("' + lang + '")')
    return str_readme
