import re
import emoji
import locale


def remove_markup(text):
    """ Remove hyperlinks and markup """
    result = re.sub("<[a][^>]*>(.+?)</[a]>", 'Link.', text)
    result = re.sub('&gt;', "", result)
    result = re.sub('&#x27;', "'", result)
    result = re.sub('&quot;', '"', result)
    result = re.sub('&#x2F;', ' ', result)
    result = re.sub('<p>', ' ', result)
    result = re.sub('</i>', '', result)
    result = re.sub('&#62;', '', result)
    result = re.sub('<i>', ' ', result)
    result = re.sub("\n", '', result)
    return result


def remove_emoticons(text):
    emoticon_string = r"(?:[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP\/\:\}\{@\|\\]+|[\)\]\(\[dDpP\/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?)"
    return re.sub(emoticon_string, '', text)


def replace_price_with_placeholder(text):
    """
    Replaces price with placeholder
    :param text: string to clean
    :return: cleaned string
    """
    text = re.sub(r'\d+(?:[.,]\d+)? ?[$€£¥₩₹₽₿]+', 'peněz', text)
    return text


def clean(text):
    """
    Removes unnecessary whitespaces, characters, emoticons, non ASCII characters, punctuation, normalizes to lowercase.
    :param text: string to clean
    :return: cleaned string
    """
    text = remove_markup(text)
    text = emoji.replace_emoji(text)
    text = remove_emoticons(text)
    text = replace_price_with_placeholder(text)

    # remove non-ascii characters except czech and slovak characters
    text = re.sub(r'[^\x00-\x7FáäčďéěíĺľňóôŕřšťúůýžÁÄČĎÉĚÍĹĽŇÓÔŔŘŠŤÚŮÝŽ:,.!?]+', ' ', text)

    # remove duplicate punctuation
    text = re.sub(r'([:,.!?]){2,}', r'\1', text)

    return text