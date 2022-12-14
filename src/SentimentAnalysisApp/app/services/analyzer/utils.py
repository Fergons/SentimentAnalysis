import re
import emoji



def remove_emoticons(text):
    emoticon_string = r"(?:[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP\/\:\}\{@\|\\]|[\)\]\(\[dDpP\/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?)"
    return re.sub(emoticon_string, '', text)


def clean(text):
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
    for punc in '"\'*+-/<=>?@[\\]^_`{|}~':
        text = text.replace(punc, ' ')
    # remove duplicate punctuation
    text = re.sub(r'([!?.():]){2,}', r'\1', text)

    return text
