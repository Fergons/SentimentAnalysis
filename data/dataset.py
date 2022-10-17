import json
import re
from transformers import AutoTokenizer
from nltk import tokenize
import pandas as pd


# sentences = tokenize.sent_tokenize("I po takové době od vydání hra vypadá dobře, hraje se ještě líp a to hlavní, dostává stále nový obsah. Tuto hru mohu velice doporučit pro hráče, kteří hledají taktičtější Counter-Strike.", language="czech")


# tokenizer = AutoTokenizer.from_pretrained("ufal/robeczech-base")


def fill_in_missing_data(data):
    """
    Assigns ids to reviews.
    Fills in missing data that can be derived from present data.
    :param data: data from json string
    :return: data with filled in missing values
    """
    id_counter = 0
    for set_of_reviews in data["dataset"]:
        for review in set_of_reviews["reviews"]:
            review_id = review.get("reviewId")
            review_text = review.get("text")
            terms = review.get("aspectTerms", [])
            review["reviewId"] = id_counter

            id_counter += 1

            for term in terms:
                if term.get("from") == 0 and term.get("to") == 0:
                    word_seq = term.get("term")
                    if word_seq is not None and word_seq != "":
                        try:
                            span = re.search(word_seq, review_text).span()
                        except AttributeError:
                            print(word_seq, " ", review_text, "\n")
                            raise
                        else:
                            term["from"] = span[0]
                            term["to"] = span[1]

    with open("annotated_reviews_czech_filled.json", "w", encoding="utf_8") as fopen:
        json.dump(data, fopen, ensure_ascii=False)

    return data


def clean_text(texts):
    """
    Removes unnecessary whitespaces, characters, emoticons, non ASCII characters, punctuation, normalizes to lowercase.
    :param texts: list of texts to clean
    :return: list of cleaned texts
    """
    pass


def data_to_dataset(texts, include_dummy_tags=False):
    # tokenizer = tokenize.TweetTokenizer()
    return [tokenize.word_tokenize(text) for text in texts]
    # return [tokenizer.tokenize(text) for text in texts]


def data_to_df(data):
    """
    Transforms annotated data from json format to dataframe.
    ...
    "dataset": [
    {
      "category": List[str],
      "reviews": List[review][
        {
          "reviewId": int,
          "text": str,
          "aspectTerms": List[term][
            {
              "term": str,
              "polarity": str,
              "from": int,
              "to": int
            }
          ],
          "aspectCategories": List[category][
            {
              "category": str,
              "polarity": str
            }
          ]
        }
      ]
    }
    {
     ...
    }
    ...
    :param data: dict data in json format
    :return: pandas.DataFrame dataframe representing data
    """
    data_new = {idx: dict_of_reviews["reviews"] for idx, dict_of_reviews in enumerate(data["dataset"])}
    data_restructured = {(i, review["reviewId"], term_id): term
         for i in data_new.keys()  # for each list of reviews
         for review in data_new[i]  # for each review in the list of reviews
         for term_id, term in enumerate(review["aspectTerms"])
         }
    df = pd.DataFrame.from_dict(
        data_restructured,
        orient='index')
    return df




def main():
    try:
        with open("annotated_reviews_czech.json", "r", encoding="utf-8") as fopen:
            data = json.load(fopen)
    except (FileNotFoundError, ValueError) as err:
        print(f"Failed to load data. Error:{err}")
    else:
        # reviews = [review["text"] for review in data["dataset"][1]["reviews"]]
        # tokenized_reviews = data_to_dataset(reviews)
        # print(" ============ \n")
        # print(f" Num of reviews: {len(tokenized_reviews)} \n")
        # print(f" Samples:\n")
        # for r in tokenized_reviews[5:10]:
        #     print(r)
        # print(" ============ \n")
        # fill_in_missing_data(data)
        df = data_to_df(data)
        pd.set_option('display.max_columns', 10)
        print(df.groupby("polarity").describe(include="object"))


if __name__ == "__main__":
    main()
