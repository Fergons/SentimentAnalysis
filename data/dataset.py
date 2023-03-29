import json
import os
import re
from typing import List, Union

import emoji
import pandas as pd
import sys
import random
import string
import argparse
from nltk import tokenize
from pydantic import BaseModel

MY_DATASET = "D://PythonProjects//SentimentAnalysis//data//filled_annotated_reviews_czech.json"


class AspectTerm(BaseModel):
    term: str
    category: str
    polarity: str

    def has_term(self):
        return self.term != ""

    def __str__(self):
        term = self.term
        if term == "":
            term = "noterm"
        return f"{term}:{self.category}:{self.polarity}"


class AspectCategory(BaseModel):
    category: str
    polarity: str


class Review(BaseModel):
    reviewId: int
    text: str
    aspectTerms: List[AspectTerm]
    aspectCategories: List[AspectCategory]

    def num_aspect_terms(self):
        return len(self.aspectTerms)

    def num_aspect_categories(self):
        return len(self.aspectCategories)

    def talks_about_category(self, category):
        if type(category) == str:
            return category in [term.category for term in self.aspectTerms]
        elif type(category) == list:
            return any(c in [term.category for term in self.aspectTerms] for c in category)
        else:
            raise TypeError("Category must be of type str or list")

    def has_only_aspects_with_polarity(self, polarity):
        return all(term.polarity == polarity for term in self.aspectTerms)

    def get_string_from_aspect_terms(self):
        if self.num_aspect_terms() == 0:
            return "noaspects:none:none"
        return ", ".join([str(term) for term in self.aspectTerms])


class Dataset(BaseModel):
    category: List[str]
    reviews: List[Review]

    def num_reviews(self):
        return len(self.reviews)

    def has_category(self, category):
        if type(category) == str:
            return category in self.category
        elif type(category) == list:
            return any(c in self.category for c in category)
        else:
            raise TypeError("Category must be of type str or list")

    def only_reviews_of_polarity(self, polarity):
        return [review for review in self.reviews
                if review.has_only_aspects_with_polarity(polarity) and review.num_aspect_terms() > 0]


class Data(BaseModel):
    dataset: List[Dataset]

    def num_datasets(self):
        return len(self.dataset)

    def get_all_reviews(self):
        return [review for dataset in self.dataset for review in dataset.reviews]

    def get_positive_reviews(self):
        return [review for dataset in self.dataset for review in dataset.only_reviews_of_polarity("positive")]

    def get_negative_reviews(self):
        return [review for dataset in self.dataset for review in dataset.only_reviews_of_polarity("negative")]

    def get_neutral_reviews(self):
        return [review for dataset in self.dataset for review in dataset.only_reviews_of_polarity("neutral")]

    def get_reviews_with_no_aspect(self):
        return [review for dataset in self.dataset for review in dataset.reviews if review.num_aspect_terms() == 0]

    def get_reviews_for_category(self, category: Union[str, list]):
        return [review for dataset in self.dataset for review in dataset.reviews if dataset.has_category(category)]


def get_my_dataset() -> Data:
    """Gets my dataset."""
    dataset = load_json_data(file=MY_DATASET)
    return Data(**dataset)


def get_annotated_reviews():
    """Gets annotated reviews from the dataset."""
    return get_all_reviews_from_dataset(get_my_dataset().dict())


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


def instruct2pyabsa(file_in="validation/FPS_generated_data.txt", file_out="validation/FPS_generated_data_pyabsa.txt"):
    """transforms the data into the format of PyABSA"""
    with open(file_in, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(file_out, "w", encoding="utf-8") as f:
        print("Converting data to PyABSA format...")
        for line in lines:
            if line.startswith("Input: "):
                text = line[7:].strip()
            elif line.startswith("Output: "):
                aspects_str = line[8:]
                aspects = aspects_str.split(",")
                for aspect in aspects:
                    aspect = aspect.strip().split(":")
                    term = aspect[0]
                    if term in ("noaspects", "none", "noterm"):
                        continue
                    category = aspect[1]
                    polarity = aspect[2]
                    if len(aspect) > 3:
                        opinion = aspect[3]
                    text_with_placeholder = text.replace(term, "$T$")
                    if text_with_placeholder == text:
                        print("Term not found in text: ", term, " ", text)
                        continue
                    # # find the term in the text
                    # num_words_of_term = len(term.split(" "))
                    # # create a list of all sequences of words of length num_words_of_term in text
                    # text_words = text.split(" ")
                    # # clean text words from punctuation
                    # text_words = [word.strip(string.punctuation) for word in text_words]
                    # if num_words_of_term > 1:
                    #     text_sequences = [" ".join(text_words[i:i + num_words_of_term]) for i in range(len(text_words) - num_words_of_term + 1)]
                    # else:
                    #     text_sequences = text_words
                    # print(text_sequences)
                    # # find the sequence that matches the term
                    # seq, score = process.extractOne(term, text_sequences)
                    # print(term, " ", seq, " ", score)
                    # # index of the sequence in the list of sequences
                    # # regex replace
                    # text_with_placeholder = text.replace(seq, "$T$", 1)
                    # # text_replaced_aspect = text.replace(term, "$T$", 1)
                    if aspect != "":
                        f.write(text_with_placeholder)
                        f.write("\n")
                        f.write(term)
                        f.write("\n")
                        f.write(polarity.capitalize())
                        f.write("\n")
    print("Saved to ", file_out)


def instruct2sentences(file_in="validation/FPS_generated_data.txt",
                       file_out="validation/FPS_generated_data_sentence.txt"):
    """transforms the data into the format of PyABSA"""
    with open(file_in, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(file_out, "w", encoding="utf-8") as f:
        print("Converting data to list of sentences...")
        for line in lines:
            if line.startswith("Input: "):
                text = line[7:].strip()
                f.write(text)
                f.write("\n")
        print("Saved to ", file_out)


def instruct_sample2dict(input, output):
    """transforms the sample of instruct dataset into the dictionary with keys text and labels for input/output pair"""
    labels = []
    for phrase in output.split(","):
        print(phrase)
        aspect, category, polarity, opinion, *_ = [*phrase.strip().split(":"), 'NULL', 'NULL', 'NULL', 'NULL']
        if aspect == "noaspects":
            aspect, category, polarity, opinion = "NULL", "NULL", "NULL", "NULL"
        if aspect is None or aspect == "" or aspect == "noterm":
            aspect = "NULL"

        labels.append({
            "aspect": aspect,
            "category": category,
            "polarity": polarity,
            "opinion": opinion
        })

    return {
        "text": input,
        "labels": labels
    }


def instruct2json(file_in, file_out):
    """
    Transforms the dataset from text Input:... Output:... format to json format.
    """
    if not file_out.endswith(".jsonl"):
        file_out += ".jsonl"

    with open(file_in, "r", encoding="utf-8") as f:
        lines = f.readlines()
    data = []
    for i in range(0, len(lines), 2):
        input = lines[i].strip()[7:]
        output = lines[i + 1].strip()[8:]
        data.append(instruct_sample2dict(input, output))

    with open(file_out, "w", encoding="utf-8") as f:
        for sample in data:
            json.dump(sample, f, ensure_ascii=False)
            f.write("\n")


def mydataset2acos(file_in, file_out):
    """
    Transforms the dataset from json format to acos format.
    """
    if not file_out.endswith(".jsonl"):
        file_out += ".jsonl"

    data = load_json_data(file_in)
    dataset = Data(**data)

    reviews = dataset.get_all_reviews()
    random.shuffle(reviews)

    with open(file_out, "w", encoding="utf-8") as f:
        for review in reviews:
            text = review.text
            aspects = review.aspectTerms
            labels = []
            for aspect in aspects:
                term = aspect.term
                polarity = aspect.polarity
                category = aspect.category
                opinion = "NULL"
                if term == "" or term is None:
                    term = "NULL"
                if category is None or category == "":
                    category = "NULL"
                if polarity is None or polarity == "":
                    polarity = "NULL"
                labels.append({"aspect": term, "category": category, "polarity": polarity, "opinion": opinion})
            sample = {"text": text, "labels": labels}
            json.dump(sample, f, ensure_ascii=False)
            f.write("\n")


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
    reviews = get_all_reviews_from_dataset(dataset)
    for review in reviews:
        terms = review.get("aspectTerms", [])
        for term in terms:
            main_category = map_category_to_main_category(term["category"])
            term["category"] = main_category
    return dataset


def map_category_to_main_category(category):
    category_map = {
        'gameplay': ['gameplay', 'game mode', 'story', 'level design',
                     'multiplayer', 'violence', 'character design',
                     'controls', 'tutorial', 'quality', 'gun play', 'gunplay', 'environment', 'gameplay mechanics',
                     'world',
                     'game environment', 'game design', 'difficulty', 'content', 'cosmetic content', 'in-game content',
                     'options', 'user interface','UI', 'interface', 'gameplay', 'game modes', 'gameplay features', 'monetization'],
        'price': ['price'],
        'audio_visuals': ['audio_visuals', 'visuals', 'sounds', 'game environment', 'game design', 'visual', 'sound',
                          'audio_visuals', 'graphics', 'music', 'soundtrack', 'sound effects', 'audio'],
        'performance_bugs': ['performance_bugs', 'bugs', 'performance', 'saves', 'developers', 'updates', 'anticheat',
                             'update', 'patch', 'bug', 'crash', 'lag', 'performance', 'server', 'servers',
                             'server issues', 'server performance'],
        'community': ['languages', 'reviews', 'community', 'comparison'],
        'overall': ['overall', 'genre', 'platform', 'game'],
        'NULL': ['NULL', 'none', None, 'null', '', 'noterm']
    }
    for main_category, subcategories in category_map.items():
        if category in subcategories:
            return main_category
    return 'other'


def reduce_categories(file_in, file_out, label="labels"):
    """
    Reduces the number of categories by grouping similar categories together.
    :param file_in: path to input json file
    :param file_out: path to output json file
    """
    with open(file_in, "r", encoding="utf-8") as f:
        lines = f.readlines()
        data = [json.loads(line) for line in lines]

    if data[0].get(label) is not None:
        pass
    elif data[0].get("labels") is not None:
        label = "labels"
    elif data[0].get("aspectTerms") is not None:
        label = "aspectTerms"
    else:
        raise ValueError(f"No known labels found in dataset and the specified label (\"{label}\") is not valid.")

    with open(file_out, "w", encoding="utf-8") as f:
        for sample in data:
            aspects = sample.get(label)
            for aspect in aspects:
                aspect["category"] = map_category_to_main_category(aspect["category"])
            json.dump(sample, f, ensure_ascii=False)
            f.write("\n")


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

    # remove links
    text = re.sub(r'https?\S+', '', text)

    # remove markup tags
    text = re.sub(r'<[^>]+>', '', text)

    # remove # and @
    for punc in '"#%&\'*<=>@[\\]^_`{|}~':
        text = text.replace(punc, '')

    # duplicit punctioation
    text = re.sub(r'([!?.,:;-]){2,}', r'\1', text)
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
                if term["term"] == "":
                    term["term"] = "noaspectterm"
                else:
                    term["term"] = term["term"].lower().strip()
                term["polarity"] = term["polarity"].strip()
                term["category"] = term["category"].strip()
                if "from" in term:
                    term.pop("from")
                if "to" in term:
                    term.pop("to")
            stringified_terms = json.dumps(terms, ensure_ascii=False).replace("\"", "'").replace(": ", ":")
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
    parser.add_argument('--to_instructABSA', action="store_true",
                        help='transform to instructABSA format and save train test split')
    parser.add_argument('--instruct2pyabsa', action="store_true", help="transform instructABSA to pyabsa format")
    parser.add_argument('--instruct2sentences', action="store_true", help="transform instructABSA to list sentences")
    parser.add_argument('--instruct2json', action="store_true", help="transform instructABSA to pyabsa acos format")
    parser.add_argument('--mydataset2acos', action="store_true", help="transform my dataset to pyabsa acos format")
    parser.add_argument('--reduce_categories', action="store_true", help="translate subcategories to main categories")

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
            args.output = args.input.rsplit(".", 1)[0].join(".conll")
        save_conll_data(args.output, conll)
    elif args.fill_missing:
        if args.input == "":
            args.input = "annotated_reviews_czech.json"
        else:
            if args.input.split(".")[-1] != "json":
                raise ValueError("File doesn't seem to be a json file.")

        if args.output == "":
            args.output = args.input.rsplit(".", 1)[0].join(["filled_", ".json"])

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
            args.output = args.input.rsplit(".", 1)[0].join(["pyabsa_", ".txt"])

        dataset = dataset_to_pyabsa(load_json_data(args.input))
        save_pyabsa_data(args.output, dataset)

    elif args.clean:
        if args.input == "":
            raise ValueError("No input file chosen. --input filename")

        if args.output == "":
            args.output = args.input.rsplit(".", 1)[0].join(["cleaned_", ".txt"])

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
            train_output = args.input.rsplit(".", 1)[0].join(["train_", ".apc.txt"])
            test_output = args.input.rsplit(".", 1)[0].join(["test_", ".apc.txt"])
        else:
            train_output = args.input.rsplit(".", 1)[0].join(["train_", ".apc.txt"])
            test_output = args.input.rsplit(".", 1)[0].join(["test_", ".apc.txt"])

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
            args.output = args.input.rsplit(".", 1)[0].join(["renamed_subgroups_", ".json"])

        dataset = load_json_data(args.input)
        grouped = replace_subgroup_names_with_parent_group_name(dataset)
        save_json_data(args.output, grouped)

    elif args.to_instructABSA:
        if args.input == "":
            args.input = "annotated_reviews_czech.json"
        dataset = load_json_data(args.input)
        create_instructABSA_train_test_split(dataset)

    elif args.instruct2pyabsa:
        if args.input == "":
            print("No input file chosen. --input filename")
            return
        if args.output == "":
            args.output = args.input.rsplit(".", 1)[0].join(["pyabsa_", ".txt"])
        instruct2pyabsa(args.input, args.output)

    elif args.instruct2sentences:
        if args.input == "":
            print("No input file chosen. --input filename")
            return
        if args.output == "":
            args.output = args.input.rsplit(".", 1)[0].join(["sentences_", ".txt"])
        instruct2sentences(args.input, args.output)

    elif args.instruct2json:
        if args.input == "":
            print("No input file chosen. --input filename")
            return
        if args.output == "":
            args.output = args.input.rsplit(".", 1)[0]
        instruct2json(args.input, args.output)

    elif args.mydataset2acos:
        if args.output == "":
            args.output = args.input.rsplit(".", 1)[0]
        mydataset2acos(args.input, args.output)

    elif args.reduce_categories:
        if args.input == "":
            print("No input file chosen. --input filename")
            return
        if args.output == "":
            args.output = f"{args.input.rsplit('.', 1)[0]}.main_categories.jsonl"
        reduce_categories(args.input, args.output)


if __name__ == "__main__":
    main()
