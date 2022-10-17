import json
from transformers import AutoTokenizer
from nltk import tokenize


# sentences = tokenize.sent_tokenize("I po takové době od vydání hra vypadá dobře, hraje se ještě líp a to hlavní, dostává stále nový obsah. Tuto hru mohu velice doporučit pro hráče, kteří hledají taktičtější Counter-Strike.", language="czech")


# tokenizer = AutoTokenizer.from_pretrained("ufal/robeczech-base")



def review_to_sentences(review):
    pass

def clean_text(text):
    """
    Removes unnecessary whitespaces, characters, emoticons, non ASCII characters and punctuation.
    :param text:
    :return:
    """
    pass