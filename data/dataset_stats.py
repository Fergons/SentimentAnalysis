import pandas as pd
import json
from dataset import dataset_to_df, replace_subgroup_names_with_parent_group_name

try:
    with open("filled_annotated_reviews_czech.json", "r", encoding="utf-8") as fopen:
        data = json.load(fopen)
except (FileNotFoundError, ValueError) as err:
    print(f"Failed to load data. Error:{err}")
else:
    data = replace_subgroup_names_with_parent_group_name(data)
    df = dataset_to_df(data)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.precision', 2)
    print(df.sample(20))
    print(df.category.unique())
    print(df.groupby("category").describe(include="object"))
    print(df.groupby("polarity").describe(include="object"))
