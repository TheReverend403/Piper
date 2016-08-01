from tinydb import TinyDB, where


class Database(object):
    def __init__(self, path):
        self.db = TinyDB(path)

    def get_user_value(self, user, key):
        key = '_' + key
        table = self.db.table('user_values')
        value = table.get(where('id') == user.id)
        return value[key] if value and key in value else None

    def set_user_value(self, user, key, value):
        key = '_' + key
        table = self.db.table('user_values')
        if not table.get(where('id') == user.id):
            table.insert({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                key: value
            })
        else:
            self.update_user(user, {key: value})

    def update_user(self, user, extra_params=None):
        table = self.db.table('user_values')
        table.update({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }, where('id') == user.id)
        if extra_params is not None:
            table.update(extra_params, where('id') == user.id)

    def get_chat_value(self, chat, key):
        key = '_' + key
        table = self.db.table('chat_values')
        value = table.get(where('id') == chat.id)
        return value[key] if value and key in value else None

    def set_chat_value(self, chat, key, value):
        key = '_' + key
        table = self.db.table('chat_values')
        if not table.get(where('id') == chat.id):
            table.insert({
                'id': chat.id,
                'type': chat.type,
                'title': chat.title,
                'username': chat.username,
                'first_name': chat.first_name,
                'last_name': chat.last_name,
                key: value
            })
        else:
            self.update_chat(chat, {key: value})

    def update_chat(self, chat, extra_params=None):
        table = self.db.table('chat_values')
        table.update({
            'type': chat.type,
            'title': chat.title,
            'username': chat.username,
            'first_name': chat.first_name,
            'last_name': chat.last_name,
        }, where('id') == chat.id)
        if extra_params is not None:
            table.update(extra_params, where('id') == chat.id)
