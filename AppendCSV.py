# Append CSV's
# Jose M. Requena Plens

import glob
import pandas as pd  # To import CSV and Markdown conversion

# Get all CSV Filepaths
result = glob.glob('*/**.csv')

# Loop over files to create dictionary (Key=filepath, Value=markdown table)
dict_csv = {}
df_append = pd.DataFrame()  # To main.csv file
for file in result:

    df = pd.read_csv(file)
    df.fillna("-", inplace=True)  # Fill empty cells with "-"
    # Sort Rows by name account
    df.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
    df.to_csv(file, index = False)  # Update CSV file
    # Append CSV data to create MAIN.CSV
    df['FILEPATH'] = file
    df_append = pd.concat([df_append, df], ignore_index=True)

# Save MAIN.csv
df_append.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
df_append.to_csv("MAIN.csv", index = False)
