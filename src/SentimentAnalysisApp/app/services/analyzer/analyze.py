import re
from typing import List

from pyabsa import AspectTermExtraction as ATEPC, DeviceTypeOption, available_checkpoints
from pyabsa import TaskCodeOption
from pyabsa.framework.checkpoint_class.checkpoint_template import CheckpointManager
from transformers import AutoTokenizer
from app.models.review import Review
from nltk import sent_tokenize


# tokenizer = AutoTokenizer.from_pretrained()
# aspect_extractor.tokenizer = tokenizer
# Config manager parse checkpoint


def get_extractor():
    return ATEPC.AspectExtractor(checkpoint="lcf_atepc_1111.game_reviews_cdw_apcacc_66.67_apcf1_48.28_atef1_79.71", device=DeviceTypeOption.CPU)


# def clean(text: str):
#     """clean text from punctuation, numbers, emoticons, and other characters"""
#     # remove emojis
#     removed_emojis = re.sub(r'[^\x00-\x7F]+', '', text)
#     # remove emoticons
#     removed_emoticons = re.sub(r'[:;=8][oO\-]?[D\)\]\(\]/\\OpP]', '', removed_emojis)
#     # remove some whitespaces
#     removed_spaces = ' '.join(removed_emoticons.split())
#     # remove punctuation
#     return re.sub(r'[^\w\s]', '', removed_spaces)
#
#
# def extract_aspects(text: str, language: str = "english", extractor=None) -> List[str]:
#     if extractor is None:
#         raise ValueError("extractor is None")
#     aspects = []
#     clean_text = clean(text)
#     sentences = sent_tokenize(clean_text, language=language)
#     for sentence in sentences:
#         aspects.extend(extractor.batch_predict(sentence, pred_sentiment=True))
#     return aspects
#
#
# def analyze_text_bulk(texts: List[str], language: str = "english"):
#     """clean review.text, sentence tokenize review.text, analyze and return list of aspects"""
#     result = {}
#     extractor = get_extractor()
#     for text in texts:
#         result[text] = extract_aspects(text, language=language, extractor=extractor)
#
#
# def analyze_db_review_bulk(reviews: List[Review]):
#     """clean review.text, sentence tokenize review.text, analyze and return list of aspects"""
#     result = {}
#     extractor = get_extractor()
#     for review in reviews:
#         result[review.id] = extract_aspects(review.text, language=review.language, extractor=extractor)
#

if __name__ == '__main__':
    atepc_examples = ['Velmi dobra hra, chytlava :-) ziadne problemy s optimalizaciou ani na ziadne bugy som nenatrafil. Ked to hrate s intel pentium tak sa nepiste recenzie typu : Mam frame dropy a laguje mi to...',
                      'Určitě doporučuji ! Vývojáři se snaží s hrou pracovat a posouvat ji dále. Za mě better and better. GJ !!',
                      'Celkem vklidu hra s velmi dobrou grafikou, ale špatnou optimalizací.  :)',
                      "Bezva hra, chce to cvik ale když to baví tak se dá vydržet než si to vychytáte.Doporučuji sluchátka s mikrofonem a umět trochu anglicky, pak je hra o 100 zábavnější.",
                      "Hra je super, potrebuje ešte pár optimalizácií, ale už teraz je to najlepší Battle Royale aký som kedy hral.PS: Je to jediný Battle Royale, čo som kedy hral :D"
                      ]
    # analyze_text_bulk(atepc_examples, language='czech')
    ex = get_extractor()
    ex.batch_predict(atepc_examples, pred_sentiment=True)