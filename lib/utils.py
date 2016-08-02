import emoji

HTML_REPLACEMENTS = {
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;'
}


def telegram_escape(s):
    if type(s) is list:
        return [telegram_escape(item) for item in s]
    if type(s) is not str or not any(entity in s for entity in ['&', '<', '>', '"']):
        return s

    # Must be done first
    s = s.replace('&', '&amp;')
    for token, replacement in HTML_REPLACEMENTS.items():
        s = s.replace(token, replacement)
    return s


def emojify(text):
    if type(text) is list:
        return [emojify(item) for item in text]
    return emoji.emojize(text, use_aliases=True)


def user_to_string(user):
    pretty_user = '{0}: {1}'.format(user.id, user.first_name)
    if user.last_name:
        pretty_user += ' {0}'.format(user.last_name)
    if user.username:
        pretty_user += ' (@{0})'.format(user.username)
    return pretty_user


def chat_to_string(chat):
    if chat.type == 'private':
        return user_to_string(chat)
    pretty_chat = '{0}: [{1}]'.format(chat.id, chat.type)
    if chat.username or chat.title:
        if chat.title:
            pretty_chat += ' [{0}]'.format(chat.title)
        if chat.username:
            pretty_chat += ' (@{0})'.format(chat.username)
    return pretty_chat
