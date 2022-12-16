import asyncio
import os
import re
from typing import List

from pyabsa import (AspectPolarityClassification as APC,
                    AspectTermExtraction as ATEPC,
                    DeviceTypeOption)
from app.crud.review import crud_review
from app.db.session import async_session
from app.models.review import Review
from .utils import clean
from nltk import sent_tokenize

def get_extractor(checkpoint_name = "fast_lcf_atepc_1113.game_aug_cdw_apcacc_98.55_apcf1_98.28_atef1_74.06"):
    checkpoint_name = "fast_lcf_atepc_1113.game_aug_cdw_apcacc_98.55_apcf1_98.28_atef1_74.06"
    return ATEPC.AspectExtractor(checkpoint=f"{os.path.realpath(os.path.dirname(__file__))}/checkpoints/{checkpoint_name}", device=DeviceTypeOption.CPU)


def get_apc():
    return APC.SentimentClassifier(checkpoint="multilingual", device=DeviceTypeOption.CPU)


def extract_aspects(text: str, language: str = "english", extractor=None) -> List[str]:
    if extractor is None:
        raise ValueError("extractor is None")
    results = []
    clean_text = clean(text)
    sentences = []
    if len(clean_text) >= 256:
        _sentences = sent_tokenize(clean_text, language=language)
        _sentence = ""

        for sentence in _sentences:
            _sentence = f"{_sentence}{sentence}"
            if len(_sentence) >= 256:
                sentences.append(_sentence)
                _sentence = ""

        if len(_sentence) > 0:
            sentences.append(_sentence)
    else:
        sentences.append(clean_text)

    results.extend(extractor.batch_predict(sentences, pred_sentiment=True, print_result=True))
    return results


def analyze_db_review_bulk(reviews: List[Review]):
    """clean review.text, sentence tokenize review.text, analyze and return list of aspects"""
    result = {}
    extractor = get_extractor()
    for review in reviews:
        result[review.id] = extract_aspects(review.text, language=review.language, extractor=extractor)
    return result


async def analyze_db_reviews():
    async with async_session() as session:
        reviews = await crud_review.get_not_processed_by_source(session, source_id=1, limit=10)

    result = analyze_db_review_bulk(reviews)
    print(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(analyze_db_reviews())

    # atepc_examples = ['Velmi dobra hra, chytlava :-) ziadne problemy s optimalizaciou ani na ziadne bugy som nenatrafil. Ked to hrate s intel pentium tak sa nepiste recenzie typu : Mam frame dropy a laguje mi to...',
    #                   'Určitě doporučuji ! Vývojáři se snaží s hrou pracovat a posouvat ji dále. Za mě better and better. GJ !!',
    #                   'Celkem vklidu hra s velmi dobrou grafikou, ale špatnou optimalizací.  :)',
    #                   "Bezva hra, chce to cvik ale když to baví tak se dá vydržet než si to vychytáte.Doporučuji sluchátka s mikrofonem a umět trochu anglicky, pak je hra o 100 zábavnější.",
    #                   "Hra je super, potrebuje ešte pár optimalizácií, ale už teraz je to najlepší Battle Royale aký som kedy hral.PS: Je to jediný Battle Royale, čo som kedy hral :D"
    #                   ]
    # # atepc_examples = "Super dynamické závodění|Povedená prezentace obsahu|Ukázkové připojování do hry|Důraz na sběratele".lower().split("|")
    # # analyze_text_bulk(atepc_examples, language='czech')
    # ex = get_extractor()
    # ex.batch_predict(atepc_examples, pred_sentiment=True)
