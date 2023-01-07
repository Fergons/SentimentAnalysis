import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
from dataset import dataset_to_df, replace_subgroup_names_with_parent_group_name, get_my_dataset


def create_wordcloud(name, data):
    """
    Create wordcloud from list of data and save plt image file
    """
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(" ".join(data))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'{name}_wordcloud.png')


def create_stats_for_dataset(dataset):
    dataset = replace_subgroup_names_with_parent_group_name(dataset)
    df = dataset_to_df(dataset)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.precision', 2)


    print(df.sample(20))
    print(df.category.unique())

    print(df.groupby("category").describe(include="object"))
    print(df.groupby("polarity").describe(include="object"))

    grouped = df.groupby(['category', 'polarity'])
    print(grouped.describe(include="object"))
    grouped.count()

    wordcloud_data = get_list_of_terms_for_each_category_from_dataframe(df)
    for category, data in wordcloud_data.items():
        create_wordcloud(category, data)


def get_list_of_terms_for_each_category_from_dataframe(df):
    """
    returns dict of lists of terms for each category
    """
    result = {}
    for category in df.category.unique():
        result[category] = df[df.category == category].term.tolist()
    return result

def main():
    data = get_my_dataset()
    create_stats_for_dataset(data)

if __name__ == '__main__':
    main()

