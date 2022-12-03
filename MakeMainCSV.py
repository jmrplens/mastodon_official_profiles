# Append CSV's
# Jose M. Requena Plens

import glob
import os
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
    filename = os.path.basename(file).split('/')[-1]
    df['FILENAME'] = filename[0:len(filename)-4]  # Remove ".csv"
    df_append = pd.concat([df_append, df], ignore_index=True)

# Save MAIN.csv
df_append.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
df_append.to_csv("MAIN.csv", index = False)

# Update SVG DATABASE TOTAL PROFILES
filename = ".resources/information/DATABASE_PROFILES_NUM_EN.svg"
filenametemp = ".resources/information/DATABASE_PROFILES_NUM_TMP_EN.svg"
open(filename, 'w').write(open(filenametemp).read().replace('XXXX',str(len(df_append))))

filename = ".resources/information/DATABASE_PROFILES_NUM_ES.svg"
filenametemp = ".resources/information/DATABASE_PROFILES_NUM_TMP_ES.svg"
open(filename, 'w').write(open(filenametemp).read().replace('XXXX',str(len(df_append))))
