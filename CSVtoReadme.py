# CSV to Markdown in desired locations
# Jose M. Requena Plens
# Use the html comments to write markdown tables
# Between:
# <!-- CSV start filepath -->
# <!-- CSV end -->

import glob
import pandas as pd  # To import CSV and Markdown conversion
from minsert import MarkdownFile  # To insert Markdown in md.file

# Get all CSV Filepaths
result = glob.glob('*/**.csv')

# Loop over files to create dictionary (Key=filepath, Value=markdown table)
dict_csv = {}
df_append = pd.DataFrame()  # To main.csv file
for file in result:
    # Create Keys with filepaths and values with Markdown table
    df = pd.read_csv(file)
    df.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
    dict_csv[file] = \
        df.to_markdown(index = False) + '\n\n' + '[View .CSV](' + file + ')'
    df.to_csv(file, index = False)  # Update CSV file
    df_append = pd.concat([df_append,df], ignore_index=True)

# Save MAIN.csv
df_append.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
df_append.to_csv("MAIN.csv", index = False)

# Get .md File
file = MarkdownFile("README_ES.md")
# Refresh tables
file.insert(dict_csv)

# Get .md File
file = MarkdownFile("README_EN.md")
# Refresh tables
file.insert(dict_csv)