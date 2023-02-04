import re
from typing import List
import asyncio
import json
from collections import Counter


class Trie:
    """
    code source: https://gist.github.com/EricDuminil/8faabc2f3de82b24e5a371b6dc0fd1e0
    Regex::Trie in Python. Creates a Trie out of a list of words. The trie can be exported to a Regex pattern.
    The corresponding Regex should match much faster than a simple Regex union."""

    def __init__(self):
        self.data = {}

    def add(self, word):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[''] = 1

    def dump(self):
        return self.data

    def quote(self, char):
        return re.escape(char)

    def _pattern(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._pattern(data[char])
                    alt.append(self.quote(char) + recurse)
                except:
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append('[' + ''.join(cc) + ']')

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def pattern(self):
        return self._pattern(self.dump())


def trie_regex_from_words(words, context=False):
    trie = Trie()
    for word in words:
        trie.add(word)
    if context:
        return re.compile(r"((?:\w+[ ]+){0,2})" + trie.pattern() + r"((?:[ ]+\w+){0,3})", re.IGNORECASE)
    return re.compile(r"\b" + trie.pattern() + r"\b", re.IGNORECASE)


def find_references_in_reviews_and_context(words_to_match: List[str] = None, reviews: List[str] = None):
    """
    return reviews that contained reference to games supplied in regex list
    :param words_to_match: list of strings for names of the games you want to find reference to
    :param reviews: list of text reviews as strings
    :return: list of reviews referencing another game in regex strings with context
    """
    regex = trie_regex_from_words(words_to_match, context=True)
    return list(filter(None, [find(regex, review, context=True) for review in reviews]))


def find_references_in_reviews(words_to_match: List[str] = None, reviews: List[str] = None):
    """
    return reviews that contained reference to games supplied in regex list
    :param words_to_match: list of strings for names of the games you want to find reference to
    :param reviews: list of text reviews as strings
    :return: list of reviews referencing another game in regex strings
    """
    regex = trie_regex_from_words(words_to_match)
    return list(filter(None, [find(regex, review) for review in reviews]))


def find_references_in_review(words_to_match: List[str] = None, review: str = None):
    """
    return reviews that contained reference to games supplied in regex list
    :param words_to_match: list of strings for names of the game you want to find reference to
    :param review: text review as string
    :return: review or None
    """

    regex = trie_regex_from_words(words_to_match)
    return find(regex, review)


def find(regex: re.Pattern = None, review: str = None, context: bool = False):
    if context:
        match = regex.search(review)
        if match is None:
            return None
        return {"review": review, "context": match.groups()}
    else:
        match = regex.findall(review)
        if len(match) == 0:
            return None
        # print(match)
        return review

def xtest1(words, file):
    with open(file, encoding="utf-8") as fopen:
        reviews = json.load(fopen)
    print(len(reviews))
    reviews_with_references = find_references_in_reviews(words_to_match=words, reviews=reviews)
    print(len(reviews_with_references))


def get_comparisons_to_other_games_stats(name, words, file):
    with open(file, encoding="utf-8") as fopen:
        reviews = json.load(fopen)
    filtered_reviews = [ review for review in reviews if len(review.split(" ")) > 1]
    reviews_with_references = find_references_in_reviews(words_to_match=words, reviews=reviews)
    with open(f"comparisons_in_{name}.txt", "w", encoding="utf8") as fopen:
        fopen.write("-"*30)
        fopen.write(f"\nReviews: {file}\n\n")
        fopen.write(f"Number of reviews: {len(reviews)}\n")
        fopen.write(f"Number of filtered reviews: {len(reviews)}\n")
        fopen.write(f"Number of reviews with reference: {len(reviews_with_references)}\n")
        fopen.write(f"Percentile: {round(len(reviews_with_references)/len(reviews)*100,2)}%\n")
        fopen.write(f"Percentile(filtered): {round(len(reviews_with_references)/len(filtered_reviews)*100,2)}%\n")
        fopen.write("-" * 30)

        for review in reviews_with_references:
            fopen.write("-"*50)
            fopen.write(f"\n{review}\n")

    return reviews_with_references

def get_context(words, file) -> object:
    with open(file, encoding="utf-8") as fopen:
        reviews = json.load(fopen)
    print(len(reviews))
    context = [r.get("context") for r in find_references_in_reviews_and_context(words_to_match=words, reviews=reviews)]
    before_context = list(filter(None, [x[0].strip() for x in context]))
    after_context = list(filter(None, [x[1].strip() for x in context]))
    print("before: ", before_context)
    print("after: ", after_context)
    print(len(context))
    print(len(before_context))
    print(len(after_context))
    return before_context, after_context


def xtest2():
    """
    finds most popular comparison phrases and prints some aspects
    """
    before_context, after_context = get_context(
        ["BF4", "BF3", "battlefield", "valorant", "GTA", "COD", "konter", "csgo", "cs", "csko", "cska", "csku", "gocko",
         "gocku",
         "gočku", "gočko", "gočka", "cs:go", "cs go", "counter", "call of duty", "codko", "MW4", "overwatch", "OW"],
        "appid_359550_czech.json")
    counter = Counter(before_context)
    print(dict(counter.most_common(10)).keys())
    # subject_maybe_before, subject_maybe_after = get_context(before_context, "appid_359550_czech.json")
    subject_maybe_before, subject_maybe_after = get_context([c[0] for c in counter.most_common(5)],
                                                            "appid_359550_czech.json")
    counter = Counter(subject_maybe_after)
    print(counter)


def xtest3():
    before, after = get_context(
        ["oproti", "lepší než", "lepší jak", "better than", "Better than", "better then", "než v", "lepsi nez",
         "to jako", "hra jak", "game like"], "appid_578080_czech.json")
    counter = Counter(after)
    print(counter)

if __name__ == "__main__":
    # most common comparison phrases ["oproti","lepší než", "lepší jak", "better than", "Better than", "better then", "než v", "lepsi nez", "to jako", "hra jak", "game like"]

    # test1(["ARC survival", "fofrnajt","PUBG",'fortnite',"H1Z1","BF4","BF3","battlefield","valorant","GTA","COD", "konter","csgo","cs","csko","cska","csku","gocko","gocku","gočku","gočko","gočka","cs:go","cs go", "counter", "call of duty", "codko", "MW4", "overwatch", "OW"], "appid_359550_czech.json")

    # test1(["counter"], "appid_359550_czech.json"
    # for r6s ["ARC", "fofrnajt", "PUBG", 'fortnite', "H1Z1", "BF2042", "BF1","BF4", "BF3", "battlefield", "valorant", "GTA", "COD", "konter","csgo", "cs", "csko", "cska", "csku", "gocko", "gocku", "gočku", "gočko", "gočka", "cs:go", "cs go", "counter","call of duty", "codko", "MW4", "overwatch", "OW"]
    # for cod ["ARC", "fofrnajt","PUBG",'fortnite',"H1Z1", "BF2042". "BF1","BF4","BF3","battlefield","valorant","GTA","COD", "konter","csgo","cs","csko","cska","csku","gocko","gocku","gočku","gočko","gočka","cs:go","cs go", "counter", "MW4", "overwatch", "OW"]
    # for pubg ["ARC", "fofrnajt", 'fortnite', "H1Z1", "BF2042","BF4",  "BF1", "BF3", "battlefield", "valorant", "GTA", "COD", "konter","csgo", "cs", "csko", "cska", "csku", "gocko", "gocku", "gočku", "gočko", "gočka", "cs:go", "cs go", "counter","call of duty", "codko", "MW4","war zone", "overwatch", "OW"]

    #for file in ("appid_359550_czech.json","appid_578080_czech.json","appid_1938090_czech.json"):
    # for r6s
    print("R6S")
    get_comparisons_to_other_games_stats("R6S",
        ["ARC", "fofrnajt", "PUBG", 'fortnite', "H1Z1", "BF2042", "BF1","BF4", "BF3", "battlefield", "valorant", "GTA", "COD", "konter","csgo", "cs", "csko", "cska", "csku", "gocko", "gocku", "gočku", "gočko", "gočka", "cs:go", "cs go", "counter","call of duty", "codko", "MW4", "overwatch", "OW"]+["oproti", "lepší než", "lepší jak", "better than", "Better than", "better then", "než v", "lepsi nez",
         "to jako", "hra jak", "game like","horsi nez","horší než"], "appid_359550_czech.json")
    #for pubg
    print("PUBG")
    get_comparisons_to_other_games_stats("PUBG",
        ["ARC", "fofrnajt", 'fortnite', "H1Z1", "BF2042","BF4",  "BF1", "BF3", "battlefield", "valorant", "GTA", "COD", "konter","csgo", "cs", "csko", "cska", "csku", "gocko", "gocku", "gočku", "gočko", "gočka", "cs:go", "cs go", "counter","call of duty", "codko", "MW4","war zone", "overwatch", "OW"]+["oproti", "lepší než", "lepší jak", "better than", "Better than", "better then", "než v", "lepsi nez",
         "to jako", "hra jak", "game like","horsi nez","horší než"], "appid_578080_czech.json")
    # for cod
    print("COD")
    get_comparisons_to_other_games_stats("COD",
        ["ARC", "fofrnajt", "PUBG", 'fortnite', "H1Z1", "BF2042", "BF1", "BF4", "BF3", "battlefield", "valorant", "GTA",
         "konter", "csgo", "cs", "csko", "cska", "csku", "gocko", "gocku", "gočku", "gočko", "gočka", "cs:go",
         "cs go", "counter", "MW4", "overwatch", "OW"]+["oproti", "lepší než", "lepší jak", "better than", "Better than", "better then", "než v", "lepsi nez",
         "to jako", "hra jak", "game like","horsi nez","horší než"], "appid_1938090_czech.json")

