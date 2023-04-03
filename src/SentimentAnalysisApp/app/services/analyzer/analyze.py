import asyncio
import os
import re
from typing import List
from .utils import clean
from nltk import sent_tokenize


def get_extractor(checkpoint_name="fast_lcf_atepc_1113.game_aug_cdw_apcacc_98.55_apcf1_98.28_atef1_74.06"):
    from pyabsa import AspectTermExtraction as ATEPC
    if checkpoint_name is None:
        checkpoint_name = "fast_lcf_atepc_1113.game_aug_cdw_apcacc_98.55_apcf1_98.28_atef1_74.06"
    return ATEPC.AspectExtractor(
        checkpoint=f"{os.path.realpath(os.path.dirname(__file__))}/checkpoints/{checkpoint_name}",
        device="cpu")


def get_apc():
    from pyabsa import AspectPolarityClassification as APC
    return APC.SentimentClassifier(checkpoint="multilingual", device="cpu")


def extract_aspects(text: str, language: str = "english", extractor=None) -> List[str]:
    if extractor is None:
        raise ValueError("extractor is None")
    clean_text = clean(text)
    print(f"clean_text {clean_text}")
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
    print(f"sentences {sentences}")
    results = extractor.batch_predict(sentences, pred_sentiment=True, print_result=True, save_to_file=False)
    return results


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(analyze_db_reviews())

    atepc_examples = ["Nostalgická hra. Portal jsem hrával už jako malej zmrd na bráchovo pc když byl náhodou dýl ve škole nebo venku. I teď mi nějaký level dělá problém :D nejlíp utracených 0,99€ :DD",
        'Velmi dobra hra, chytlava :-) ziadne problemy s optimalizaciou ani na ziadne bugy som nenatrafil. Ked to hrate s intel pentium tak sa nepiste recenzie typu : Mam frame dropy a laguje mi to...',
                      'Určitě doporučuji ! Vývojáři se snaží s hrou pracovat a posouvat ji dále. Za mě better and better. GJ !!',
                      'Celkem vklidu hra s velmi dobrou grafikou, ale špatnou optimalizací.  :)',
                      "Bezva hra, chce to cvik ale když to baví tak se dá vydržet než si to vychytáte.Doporučuji sluchátka s mikrofonem a umět trochu anglicky, pak je hra o 100 zábavnější.",
                      "Hra s výborným potenciálem a věřím že to ještě dotáhnou ke konci, momentálně je herní fyzika/bugy/movement poměrně špatný, prostě na začátku a jde to i vidět, bohužel mě osobně navíc to házelo eror a hra se vypínala, bohužel tam není ani zatím automatické nebo manuální uložení takže jsem tu hru nedohrál tam kam jsem teoretický mohl, ale sadismus, nekorektnost v tom tomu dodává svojí šťávu která tuhle hru požene snad jen vpřed, je to na dobré cestě :)"
                      ]
    # # atepc_examples = "Super dynamické závodění|Povedená prezentace obsahu|Ukázkové připojování do hry|Důraz na sběratele".lower().split("|")
    # analyze_text_bulk(atepc_examples, language='czech')
    ex = get_extractor(checkpoint_name="fast_lcf_atepc_1110.game_reviews_cdw_apcacc_90.36_apcf1_86.18_atef1_84.1")
    # extract_aspects("the game is good but has really bad  mechanics and lots of bugs.", extractor=ex)
    ex.batch_predict("D:\PythonProjects\SentimentAnalysis\data\sentences_.txt", pred_sentiment=True, print_result=True, save_to_file=True)
