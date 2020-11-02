"""
Run this if not run already

This script will convert excel file to csv which we will read and write from
"""
import pandas as pd

file_location = "assets/Section_4.xlsx"
new_file = "assets/Section_4.csv"


read_file = pd.read_excel(file_location)
read_file.to_csv(new_file, index=None, header=True)
