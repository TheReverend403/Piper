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
        if table.get(where('id') == user.id):
            table.update({
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                key: value
            }, where('id') == user.id)
        else:
            table.insert({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                key: value
            })

    def get_chat_value(self, chat, key):
        key = '_' + key
        table = self.db.table('chat_values')
        value = table.get(where('id') == chat.id)
        return value[key] if value and key in value else None

    def set_chat_value(self, chat, key, value):
        key = '_' + key
        table = self.db.table('chat_values')
        if table.get(where('id') == chat.id):
            table.update({
                'type': chat.type,
                'title': chat.title,
                'username': chat.username,
                'first_name': chat.first_name,
                'last_name': chat.last_name,
                key: value
            }, where('id') == chat.id)
        else:
            table.insert({
                'id': chat.id,
                'type': chat.type,
                'title': chat.title,
                'username': chat.username,
                'first_name': chat.first_name,
                'last_name': chat.last_name,
                key: value
            })
