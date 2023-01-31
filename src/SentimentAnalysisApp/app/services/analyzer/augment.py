import asyncio
import random
from typing import List
import copy
import logging

from nlpaug.util import Action
from app.services.analyzer.utils import clean
from app.db.session import async_session
from app.crud.review import crud_review
from data.dataset import get_my_dataset, dataset_to_df, get_all_reviews_from_dataset, save_pyabsa_data, dataset_to_pyabsa


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)


def substitute(texts):
    from nlpaug.augmenter.word import ContextualWordEmbsAug, SynonymAug
    """Substitutes some words in given texts with contextually similar words."""
    aug = ContextualWordEmbsAug(
        model_type='bert',
        model_path="fav-kky/FERNET-C5",
        action=Action.SUBSTITUTE,
        aug_max=4,
        aug_p=0.2)

    augmented_text = aug.augment([clean(x) for x in texts])
    return augmented_text


def generate_sentences_from_positive_and_negative_aspects(positive, negative, n=1):
    """Creates sentences from given texts."""
    from nlpaug.augmenter.word import ContextualWordEmbsAug
    aug = ContextualWordEmbsAug(
        model_type='bert',
        model_path="fav-kky/FERNET-C5",
        action=Action.INSERT,
        aug_min=1,
        aug_max=20,
        aug_p=0.6)

    pos = " a ".join(positive)
    neg = " a ".join(negative)

    # aug_pos = aug.augment(pos)
    # aug_neg = aug.augment(neg)
    sentence = f"Na hre se mi líbi {pos}, za negatíva považuji {neg}."
    return aug.augment(sentence, n=n)


async def get_positive_negative_aspects_from_db():
    """Gets good and bad aspects from the database."""
    async with async_session() as session:
        reviews = await crud_review.get_with_good_and_bad_by_language_multi(session, language="czech")
        logger.debug(f"fetched {len(reviews)} reviews from the database")
        good = []
        bad = []
        for review in reviews:
            if review.good is not None:
                good.extend(review.good.lower().split("|"))
            if review.bad is not None:
                bad.extend(review.bad.lower().split("|"))
        logger.debug(f"got {len(good)} good aspects and {len(bad)} bad aspects")
        return {
            "positive": good,
            "negative": bad
        }


def create_aspect_dictionary(positive: List[str] = None, negative: List[str] = None):
    """Creates dictionary with polarities of aspects from given positive and negative aspects."""
    neutral = []
    new_positive = []
    new_negative = []
    logger.debug(len(positive))
    for aspect in positive:
        length = len(aspect.split(" "))
        if length == 1:
            neutral.append(clean(aspect))
        elif length < 4:
            new_positive.append(clean(aspect))

    for aspect in negative:
        length = len(aspect.split(" "))
        if length < 4:
            new_negative.append(clean(aspect))

    return {
        "positive": new_positive,
        "negative": new_negative,
        "neutral": neutral
    }


def substitute_review_aspects(review, old_aspects, new_aspects):
    """substitutes aspect terms in text on matching sentiment."""
    for aspect, new_aspect in zip(old_aspects, new_aspects):
        review = review.replace(aspect, new_aspect)
    return review


def augment_reviews_with_aspects(reviews, aspects=None):
    """Augments given reviews by matching labeled aspects."""
    augmented_reviews = []
    for review in reviews:
        review.get("terms")
    return augmented_reviews


async def augment_my_dataset():
    """Augments my dataset with aspects from the database."""
    reviews = get_all_reviews_from_dataset(get_my_dataset())
    aspect_dict = await get_positive_negative_aspects_from_db()
    aspect_dict = create_aspect_dictionary(**aspect_dict)

    logger.debug(f"Reviews: {len(reviews)}")
    logger.debug(f"Positive aspects: {len(aspect_dict['positive'])}")
    logger.debug(f"Negative aspects: {len(aspect_dict['negative'])}")
    logger.debug(f"Neutral aspects: {len(aspect_dict['neutral'])}")

    neutral = aspect_dict["neutral"]
    positive = aspect_dict["positive"]
    negative = aspect_dict["negative"]
    neutral2 = copy.deepcopy(neutral)

    random.shuffle(neutral)
    random.shuffle(neutral2)
    random.shuffle(positive)
    random.shuffle(negative)

    new_reviews = []

    while len(neutral2) > 0 and len(positive) > 0 and len(negative) > 0:
        for review in reviews:
            review = copy.deepcopy(review)
            aspects = review.get("aspectTerms")

            old_terms = []
            new_terms = []
            num = random.randint(0, len(aspects))

            for _ in range(num):
                idx = random.randint(0, len(aspects)-1)
                aspect = aspects[idx]

                term = aspect.get("term")
                polarity = aspect.get("polarity")
                if term == "":
                    continue
                old_terms.append(term)
                new_term = term
                if len(neutral) > 0:
                    new_term = neutral.pop()

                elif polarity == "positive":
                    if len(positive) > 0:
                        new_term = positive.pop()

                elif polarity == "negative":
                    if len(negative) > 0:
                        new_term = negative.pop()

                elif polarity == "neutral":
                    if len(neutral2) > 0:
                        new_term = neutral2.pop()

                aspect["term"] = new_term
                new_terms.append(new_term)

            review["text"] = substitute_review_aspects(review.get("text"), old_terms, new_terms)
            new_reviews.append(review)
    return new_reviews


async def main():
    dataset = await augment_my_dataset()
    random.shuffle(dataset)
    train = dataset[:int(len(dataset) * 0.7)]
    valid = dataset[int(len(dataset) * 0.7):int(len(dataset) * 0.85)]
    test = dataset[int(len(dataset) * 0.85):]

    save_pyabsa_data("pyabsa_augmented_train.txt", dataset_to_pyabsa(train))
    save_pyabsa_data("pyabsa_augmented_valid.txt", dataset_to_pyabsa(valid))
    save_pyabsa_data("pyabsa_augmented_test.txt", dataset_to_pyabsa(test))


if __name__ == "__main__":

    positive_examples = "Super dynamické závodění|Povedená prezentace obsahu|Ukázkové připojování do hry|Důraz na sběratele".lower().split("|")
    negative_examples = "Nutnost připojení k internetu|Mikrotransakce".lower().split("|")
    atepc_examples = ['Velmi dobra hra, chytlava :-) ziadne problemy s optimalizaciou ani na ziadne bugy som nenatrafil. Ked to hrate s intel pentium tak sa nepiste recenzie typu : Mam frame dropy a laguje mi to...',
                      'Určitě doporučuji ! Vývojáři se snaží s hrou pracovat a posouvat ji dále. Za mě better and better. GJ !!',
                      "Bezva hra, chce to cvik ale když to baví tak se dá vydržet než si to vychytáte.Doporučuji sluchátka s mikrofonem a umět trochu anglicky, pak je hra o 100 zábavnější.",
                      "Hra je super, potrebuje ešte pár optimalizácií, ale už teraz je to najlepší Battle Royale aký som kedy hral.PS: Je to jediný Battle Royale, čo som kedy hral :D"
                      ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())