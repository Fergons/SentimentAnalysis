import pandas as pd
import json
from dataset import data_to_df

try:
    with open("annotated_reviews_czech_filled.json", "r", encoding="utf-8") as fopen:
        data = json.load(fopen)
except (FileNotFoundError, ValueError) as err:
    print(f"Failed to load data. Error:{err}")
else:
    df = data_to_df(data)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.precision', 2)
    print(df.groupby("polarity").describe(include="object"))
