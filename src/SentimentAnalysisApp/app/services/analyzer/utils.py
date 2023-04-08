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
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    # remove graphical emoji
    text = emoji.replace_emoji(text)
    # remove textual emoji
    emoticon_string = r"(?:[<>]?[:x;=8][\-o\*\']?[\)\]\(\[dDpP\/\:\}\{@\|\\]|[\)\]\(\[dDpP\/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?|<3)"
    text = re.sub(emoticon_string, '', text)
    # remove links
    text = re.sub(r'https?\S+', '', text)
    # remove formatting
    # input: [h1] lorem ipsum [\h1]
    # output: lorem ipsum
    text = re.sub(r'\[[^]]*?]', '', text)
    # remove non alphanumeric characters except for some punctuation
    text = re.sub(r'[^\w\d ().,?!-;\']', '', text)
    return text
