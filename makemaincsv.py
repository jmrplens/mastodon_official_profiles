# Append CSV's
# Jose M. Requena Plens

import glob
import os
import pandas as pd  # To import CSV and Markdown conversion

def makecsv() -> None:
    """Make MAIN.csv"""
    # Get all CSV Filepaths
    result = glob.glob('*/**.csv')

    # Loop over files to create dictionary (Key=filepath, Value=markdown table)
    df_append = pd.DataFrame()  # To main.csv file
    for file in result:
        DF = pd.read_csv(file)
        DF.fillna("-", inplace=True)  # Fill empty cells with "-"
        # Sort Rows by name account
        DF.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
        DF.to_csv(file, index = False)  # Update CSV file
        # Append CSV data to create MAIN.CSV
        DF['FILEPATH'] = file
        filename = os.path.basename(file).split('/')[-1]
        DF['FILENAME'] = filename[0:len(filename)-4]  # Remove ".csv"
        df_append = pd.concat([df_append, DF], ignore_index=True)

    # Save MAIN.csv
    df_append.sort_values(by='Name', inplace=True, key=lambda col: col.str.lower())
    df_append.to_csv("MAIN.csv", index = False)
