import pandas as pd
from wordcloud import WordCloud, get_single_color_func
from collections import Counter
import matplotlib.pyplot as plt
import json
from dataset import dataset_to_df, replace_subgroup_names_with_parent_group_name, get_my_dataset

class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


def create_wordcloud(name, data):
    """
    Create wordcloud from list of data and save plt image file
    """
    terms = data.get("positive", []) + data.get("negative", []) + data.get("neutral", [])
    term_fq = Counter(terms)

    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=12).generate_from_frequencies(term_fq)

    # rename keys in data to match colors
    color_to_words = {
        "red": data.get("negative", []),
        "green": data.get("positive", []),
        "grey": data.get("neutral", [])
    }

    wordcloud.recolor(color_func=GroupedColorFunc(color_to_words=color_to_words, default_color="grey"))
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

    # wordcloud_data = get_list_of_terms_for_each_category_from_dataframe(df)
    wordcloud_data = get_terms_for_each_category_grouped_by_polarity(df)

    for category, data in wordcloud_data.items():
        create_wordcloud(category, data)

def get_terms_for_each_category_grouped_by_polarity(df):
    """
    returns dict of lists of terms for each category
    """
    result = {}
    group = df.groupby(['category', 'polarity'])
    for category in df.category.unique():
        result[category] = {}
        for polarity in df.polarity.unique():
            try:
                terms = group.get_group((category, polarity)).term.tolist()
                filtered_terms = [term for term in terms if len(term) > 1]
                result[category][polarity] = filtered_terms
            except KeyError:
                result[category][polarity] = []
    return result

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

