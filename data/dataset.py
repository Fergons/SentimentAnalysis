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

MY_DATASET = "E://PythonProjects//SentimentAnalysis//data//filled_annotated_reviews_czech.json"


def get_my_dataset():
    """Gets my dataset."""
    return load_json_data(file=MY_DATASET)


def get_annotated_reviews():
    """Gets annotated reviews from the dataset."""
    return get_all_reviews_from_dataset(get_my_dataset())


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
                        except AttributeError as e:
                            print(word_seq, " ", review_text, "\n")
                            raise e
                        else:
                            term["from"] = span[0]
                            term["to"] = span[1]
    return data


def duplicate_reviews_with_neutral_terms(dataset):
    """
    Duplicates reviews that contain aspect terms with neutral polarity.
    :param dataset: dict data in json format
    :return: dict data in json format
    """
    reviews = get_all_reviews_from_dataset(dataset)
    new_reviews = []
    for review in reviews:
        terms = review.get("aspectTerms", [])
        for term in terms:
            if term.get("polarity") == "neutral":
                new_reviews.append(review)
                new_reviews.append(review)
                break
    reviews.extend(new_reviews)
    return reviews


def remove_reviews_with_neutral_terms(dataset):
    reviews = get_all_reviews_from_dataset(dataset)
    new_reviews = []
    for review in reviews:
        neutral = False
        terms = review.get("aspectTerms", [])
        for term in terms:
            if term.get("polarity") == "neutral":
                neutral = True
                break
        if not neutral:
            new_reviews.append(review)
    return new_reviews


def replace_subgroup_names_with_parent_group_name(dataset):
    """
    Replaces subgroup names with parent group name
    :param dataset: dataset in json format
    :return: dataset with replaced subgroup names
    """
    category_map = {
        'gameplay': ['gameplay', 'game mode', 'story', 'level design',
                     'multiplayer', 'violence', 'character design',
                     'controls', 'tutorial', 'quality', 'gun play',
                     'game environment', 'game design', 'difficulty', 'content'],
        'price': ['price'],
        'audio_visuals': ['audio_visuals', 'visuals', 'sounds', 'game environment', 'game design'],
        'performance_bugs': ['performance_bugs', 'bugs', 'performance', 'saves', 'developers', 'updates', 'anticheat'],
        'community': ['languages', 'reviews', 'community', 'comparison'],
        'overall': ['overall']
    }
    reviews = get_all_reviews_from_dataset(dataset)
    for review in reviews:
        terms = review.get("aspectTerms", [])
        for term in terms:
            replaced = False
            for category, subgroups in category_map.items():
                if term.get("category", term["term"]) in subgroups:
                    term["category"] = category
                    replaced = True
                    break

            if not replaced:
                term["category"] = "other"

    return dataset


def create_train_test(dataset, train=0.8):
    reviews = dataset
    new_reviews = reviews
    train_size = int(train * len(new_reviews))

    random.shuffle(new_reviews)
    train = new_reviews[:train_size]
    test = new_reviews[train_size:]
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

    # remove # and @
    for punc in '"#$%&\'()*+-/:;<=>@[\\]^_`{|}~':
        text = text.replace(punc, '')

    # duplicit punctioation
    text = re.sub(r'([!?.,]){2,}', r'\1', text)
    return text


def dataset_to_df(dataset) -> pd.DataFrame:
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
    data_restructured = {(i, review["text"], term_id): term
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
            labels = ["O"] * len(words)
            for term in terms:
                term_words = term["term"].split(" ")
                num_term_words = len(term_words)
                term_head = term_words[0]

                for word_pos, word in enumerate(words):
                    if word == term_head:
                        labels[word_pos] = "B-A"
                        for i in range(num_term_words - 1):
                            labels[word_pos + i + 1] = "I-A"

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
        raise err
    else:
        print(f"Data saved to {file}")


def save_json_data(file, data):
    try:
        with open(file, "w", encoding="utf-8") as fopen:
            json.dump(data, fopen, ensure_ascii=False, indent=4)
    except (FileNotFoundError, ValueError) as err:
        print(f"Failed to save data.")
        raise
    else:
        print(f"Data saved to {file}")


def save_conll_data(file, dataset):
    try:
        with open(file, "w", encoding="utf-8") as fopen:
            for words, labels in dataset:
                for word, label in zip(words, labels):
                    fopen.writelines(f"{word} {label}\n")
                fopen.write("\n")
    except (FileNotFoundError, ValueError) as err:
        print(f"Failed to save data.")
        raise
    else:
        print(f"Data saved to {file}")


def get_all_reviews_from_dataset(dataset):
    return [review for dict_of_reviews in dataset["dataset"] for review in dict_of_reviews["reviews"]]


def create_instructABSA_train_test_split(dataset):
    """
    Creates instructABSA train/test split
    :param dataset: dataset as json object
    :return: train/test split of dataset
    """
    dataset = replace_subgroup_names_with_parent_group_name(dataset)
    reviews = get_all_reviews_from_dataset(dataset)
    random.shuffle(reviews)
    train_reviews = reviews[:int(len(reviews) * 0.8)]
    test_reviews = reviews[int(len(reviews) * 0.8):]
    save_instructABSA(train_reviews, "instructABSA_ACSA_train.csv")
    save_instructABSA(test_reviews, "instructABSA_ACSA_test.csv")
    return train_reviews, test_reviews


def save_instructABSA(reviews, file):
    """
    Saves reviews in instructABSA format
    raw_text,aspectTerms
    "The ambience was exceptional, but there were limitied menu options","[{'term':'ambience', 'polarity':'positive'}, {'term':'menu', 'polarity':'positive'}]"
    "The car has great mileage, but the upholsrtery wasn't classy.","[{'term':'car', 'polarity':'positive'}, {'term':'upholstery', 'polarity':'negative'}]"
    "The doctors were great, but the radiologists did a bad job with my MRI.","[{'term':'doctors', 'polarity':'positive'}, {'term':'radiologists', 'polarity':'positive'}]"
    "The shop had several laptop options","[{'term':'noaspectterm', 'polarity':'none'}]"
    :param reviews: reviews as json object
    :param file: file to save
    """
    with open(file, "w", encoding="utf-8") as fopen:
        fopen.write("raw_text\taspectTerms\n")
        for review in reviews:
            text = review["text"]
            terms = review["aspectTerms"]
            if len(terms) == 0:
                terms = [{"term": "noaspectterm", "category": "none", "polarity": "none"}]
            for term in terms:
                if term == "":
                    term["term"] = "noaspectterm"
                else:
                    term["term"] = term["term"].lower()
                if "from" in term:
                    term.pop("from")
                if "to" in term:
                    term.pop("to")
            stringified_terms = json.dumps(terms, ensure_ascii=False)
            fopen.write(f"\"{text}\"\t\"{stringified_terms}\"\n")


def main():
    parser = argparse.ArgumentParser('dataset.py')
    parser.add_argument('--input', default='', help='set dataset input file')
    parser.add_argument('--output', default='', help='set dataset output file')
    parser.add_argument('--to_conll', action="store_true", help='transform to conll and save dataset')
    parser.add_argument('--to_pyabsa', action="store_true", help='transform to pyabsa and save dataset')
    parser.add_argument('--create_train_test', action="store_true", help='split data to train and test dataset')
    parser.add_argument('--train_test_ratio', default=0.8, type=float, help='set ratio of train/test dataset')
    parser.add_argument('--init_pyabsa', action="store_true", help='initialize pyabsa dataset folder setup')
    parser.add_argument('--clean', action="store_true", help='clean reviews from input file')
    parser.add_argument('--fill_missing', action="store_true", help='fill in missing values')
    parser.add_argument('--rename_categories', action="store_true", help='renames subgroup categories to main group')
    parser.add_argument('--to_instructABSA', action="store_true", help='transform to instructABSA format and save train test split')

    args = parser.parse_args()

    if args.to_conll:
        if args.input == "":
            args.input = "annotated_reviews_czech_filled.json"
        else:
            if args.input.split(".")[-1] != "json":
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
            if args.input.split(".")[-1] != "json":
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
            if args.input.split(".")[-1] != "json":
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
            if args.input.split(".")[-1] != "json":
                raise ValueError("File doesn't seem to be a json file.")

        if args.output == "":
            train_output = args.input.split(".")[0].join(["train_", ".apc.txt"])
            test_output = args.input.split(".")[0].join(["test_", ".apc.txt"])
        else:
            train_output = args.output.split(".")[0].join(["train_", ".apc.txt"])
            test_output = args.output.split(".")[0].join(["test_", ".apc.txt"])

        train, test = create_train_test(get_all_reviews_from_dataset(load_json_data(args.input)),
                                        train=args.train_test_ratio)
        train = dataset_to_pyabsa(train)
        test = dataset_to_pyabsa(test)
        save_pyabsa_data(train_output, train)
        save_pyabsa_data(test_output, test)

    elif args.rename_categories:
        if args.input == "":
            args.input = "annotated_reviews_czech.json"
        else:
            if args.input.split(".")[-1] != "json":
                raise ValueError("File doesn't seem to be a json file.")

        if args.output == "":
            args.output = args.input.split(".")[0].join(["renamed_subgroups_", ".json"])

        dataset = load_json_data(args.input)
        grouped = replace_subgroup_names_with_parent_group_name(dataset)
        save_json_data(args.output, grouped)

    elif args.to_instructABSA:
        if args.input == "":
            args.input = "annotated_reviews_czech.json"
        else:
            if args.input.split(".")[-1] != "json":
                raise ValueError("File doesn't seem to be a json file.")
        if args.output == "":
            args.output = args.input.split(".")[0].join(["instructABSA_", ".json"])
        dataset = load_json_data(args.input)
        create_instructABSA_train_test_split(dataset)



if __name__ == "__main__":
    main()
