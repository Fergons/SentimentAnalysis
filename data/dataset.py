import json
import os
import re
import emoji
import pandas as pd
import sys
import random
import string
import argparse
from nltk import tokenize

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
    return data


def create_train_test(dataset):
    reviews = get_all_reviews_from_dataset(dataset)
    random.shuffle(reviews)
    num_train = int(len(reviews)*0.7)
    train = reviews[:num_train]
    test = reviews[num_train:]
    return train, test

def remove_emoticons(text):
    emoticon_string = r"(?:[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP\/\:\}\{@\|\\]|[\)\]\(\[dDpP\/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?)"
    return re.sub(emoticon_string, '', text)


def clean_text(text):
    """
    Removes unnecessary whitespaces, characters, emoticons, non ASCII characters, punctuation, normalizes to lowercase.
    :param text: string to clean
    :return: cleaned string
    """
    text = ' '.join(text.split())
    # remove graphical emoji
    text = emoji.replace_emoji(text)
    # remove textual emoji
    text = remove_emoticons(text)

    #remove # and @
    for punc in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
        text = text.replace(punc, '')

    return text


def dataset_to_df(dataset):
    """
    Transforms annotated dataset from json format to dataframe.
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
    :param dataset: dict data in json format
    :return: pandas.DataFrame dataframe representing data
    """
    data_new = {idx: dict_of_reviews["reviews"] for idx, dict_of_reviews in enumerate(dataset["dataset"])}
    data_restructured = {(i, review["reviewId"], term_id): term
         for i in data_new.keys()  # for each list of reviews
         for review in data_new[i]  # for each review in the list of reviews
         for term_id, term in enumerate(review["aspectTerms"])
         }
    df = pd.DataFrame.from_dict(
        data_restructured,
        orient='index')
    return df


def dataset_to_pyabsa(dataset):
    if isinstance(dataset, list):
        reviews = dataset
    else:
        reviews = get_all_reviews_from_dataset(dataset)
    dataset = []
    for review in reviews:
        text = review.get("text")
        terms = review.get("aspectTerms", [])
        for term in terms:
            word_seq = term.get("term")
            if word_seq is not None and word_seq != "":
                try:
                    new_text = re.sub(word_seq, "$T$", text)
                    dataset.append((new_text, word_seq, term.get("polarity").capitalize()))
                except AttributeError:
                    print(word_seq, " ", text, "\n")
                    raise
                else:
                    continue
    return dataset


def dataset_to_conll(dataset):
    """
            columns
    token(word)     aspect_label(ast)
    ---------------------------------
    Neuvěřitelně    O(char)
    chytlavá        0
    hratelnost      B-A
            ...
            ...
    herní           B-A
    mechanika       I-A

    :param dataset: dataset in json format see dataset_to_df
    :return: converts dataset to conll format dataset
    """
    reviews = get_all_reviews_from_dataset(dataset)
    label_tags = {0: "O", 1: "B-A", 2: "I-A"}

    conll_dataset = []
    for review in reviews:
        text = review["text"]
        if text != "":
            words = tokenize.word_tokenize(text, language="czech")
            terms = review["aspectTerms"]
            labels = ["O"]*len(words)
            for term in terms:
                term_words = term["term"].split(" ")
                num_term_words = len(term_words)
                term_head = term_words[0]

                for word_pos, word in enumerate(words):
                    if word == term_head:
                        labels[word_pos] = "B-A"
                        for i in range(num_term_words-1):
                            labels[word_pos+i+1] = "I-A"

            conll_dataset.append((words, labels))

    return conll_dataset


def load_json_data(file):
    try:
        with open(file, "r", encoding="utf-8") as fopen:
            data = json.load(fopen)
    except (FileNotFoundError, ValueError) as err:
        print(f"Failed to load data.")
        raise
    else:
        return data

def load_txt_data(file):
    try:
        with open(file, "r", encoding="utf-8") as fopen:
            data = fopen.readlines()
    except (FileNotFoundError, ValueError) as err:
        print(f"Failed to load data.")
        raise
    else:
        return data


def save_pyabsa_data(file, dataset):
    try:
        with open(file, "w", encoding="utf-8") as fopen:
            for (t, a, p) in dataset:
                fopen.write(f"{t}\n{a}\n{p}\n")
    except (FileNotFoundError, ValueError) as err:
        print(f"Failed to save data.")
        raise
    else:
        print(f"Data saved to {file}")


def save_json_data(file, data):
    try:
        with open(file, "w", encoding="utf-8") as fopen:
            json.dump(fopen, data)
    except (FileNotFoundError, ValueError) as err:
        print(f"Failed to save data.")
        raise
    else:
        print(f"Data saved to {file}")


def save_conll_data(file, dataset):
    try:
        with open(file, "w", encoding="utf-8") as fopen:
            for words, labels in dataset:
                for word, label in zip(words,labels):
                    fopen.writelines(f"{word} {label}\n")
                fopen.write("\n")
    except (FileNotFoundError, ValueError) as err:
        print(f"Failed to save data.")
        raise
    else:
        print(f"Data saved to {file}")


def get_all_reviews_from_dataset(dataset):
    return [review for dict_of_reviews in dataset["dataset"] for review in dict_of_reviews["reviews"]]


def main():
    parser = argparse.ArgumentParser('dataset.py')
    parser.add_argument('--input', default='', help='set dataset input file')
    parser.add_argument('--output', default='', help='set dataset output file')
    parser.add_argument('--to_conll', action="store_true", help='transform to conll and save dataset')
    parser.add_argument('--to_pyabsa', action="store_true", help='transform to pyabsa and save dataset')
    parser.add_argument('--create_train_test', action="store_true", help='split data to train and test dataset')
    parser.add_argument('--init_pyabsa', action="store_true", help='initialize pyabsa dataset folder setup')
    parser.add_argument('--clean', action="store_true", help='clean reviews from input file')
    parser.add_argument('--fill_missing', action="store_true", help='fill in missing values')
    parser.add_argument('--stats', action="store_true", help="get stats for polarity"),

    args = parser.parse_args()

    if args.to_conll:
        if args.input == "":
            args.input = "annotated_reviews_czech_filled.json"
        else:
            if args.input.split(".")[1] != "json":
                raise ValueError("File doesn't seem to be a json file.")
        dataset = load_json_data(args.input)
        conll = dataset_to_conll(dataset)
        if args.output == "":
            args.output = args.input.split(".")[0].join(".conll")
        save_conll_data(args.output, conll)
    elif args.fill_missing:
        if args.input == "":
            args.input = "annotated_reviews_czech.json"
        else:
            if args.input.split(".")[1] != "json":
                raise ValueError("File doesn't seem to be a json file.")

        if args.output == "":
            args.output = args.input.split(".")[0].join(["filled_", ".json"])

        dataset = fill_in_missing_data(load_json_data(args.input))
        save_json_data(args.output, dataset)

    elif args.init_pyabsa:
        from pyabsa import download_all_available_datasets
        download_all_available_datasets()

    elif args.to_pyabsa:
        if args.input == "":
            args.input = "annotated_reviews_czech.json"
        else:
            if args.input.split(".")[1] != "json":
                raise ValueError("File doesn't seem to be a json file.")

        if args.output == "":
            args.output = args.input.split(".")[0].join(["pyabsa_", ".txt"])

        dataset = dataset_to_pyabsa(load_json_data(args.input))
        save_pyabsa_data(args.output, dataset)

    elif args.clean:
        if args.input == "":
            raise ValueError("No input file chosen. --input filename")

        if args.output == "":
            args.output = args.input.split(".")[0].join(["cleaned_", ".txt"])

        if ".json" in args.input:
            list_of_reviews = load_json_data(args.input)
            cleaned = [clean_text(review) for review in list_of_reviews]
            save_json_data(args.output, cleaned)
        elif ".txt" in args.input:
            list_of_reviews = load_txt_data(args.input)
            cleaned = [f"{clean_text(review)}\n" for review in list_of_reviews]
            with open(args.output, "r", encoding="utf-8") as fopen:
                fopen.writelines(cleaned)

    elif args.create_train_test:
        if args.input == "":
            args.input = "annotated_reviews_czech.json"
        else:
            if args.input.split(".")[1] != "json":
                raise ValueError("File doesn't seem to be a json file.")

        train_output = args.input.split(".")[0].join(["train_", ".txt"])
        test_output = args.input.split(".")[0].join(["test_", ".txt"])

        train, test = create_train_test(load_json_data(args.input))
        train = dataset_to_pyabsa(train)
        test = dataset_to_pyabsa(test)
        save_pyabsa_data(train_output, train)
        save_pyabsa_data(test_output, test)

if __name__ == "__main__":
    main()
