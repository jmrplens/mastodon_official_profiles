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
for file in result:
    # Create Keys with filepaths and values with Markdown table
    df = pd.read_csv(file)
    df.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
    dict_csv[file] = \
        df.to_markdown(index = False) + '\n\n' + '[View .CSV](' + file + ')'
    df.to_csv(file, index = False)  # Update CSV file

# Get .md File
file = MarkdownFile("README.md")
# Refresh tables
file.insert(dict_csv)