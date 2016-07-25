import emoji

HTML_REPLACEMENTS = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;'
}


def telegram_escape(s):
    if type(s) is list:
        return [telegram_escape(item) for item in s]
    if type(s) is not str or not any(entity in s for entity in ['&', '<', '>', '"']):
        return s

    for k, v in HTML_REPLACEMENTS:
        s = s.replace(k, v)
    return s


def emojify(text):
    if type(text) is list:
        return [emojify(item) for item in text]
    return emoji.emojize(text, use_aliases=True)
