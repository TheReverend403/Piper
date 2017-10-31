from tinydb import TinyDB, where


class Database(object):
    def __init__(self, path):
        self.db = TinyDB(path)

    def get_user_value(self, user, key):
        key = '_' + key
        table = self.db.table('user_values')
        value = table.get(where('id') == user.id)
        try:
            return value[key]
        except KeyError:
            return None

    def set_user_value(self, user, key, value):
        self.insert_else_update_user(user, {key: value})

    def insert_else_update_user(self, user, extra_params=None):
        table = self.db.table('user_values')
        if not table.get(where('id') == user.id):
            table.insert({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            })
        else:
            table.update({
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }, where('id') == user.id)
        if extra_params:
            for k in extra_params:
                new_key = k if k.startswith('_') else '_' + k
                extra_params[new_key] = extra_params.pop(k)
            table.update(extra_params, where('id') == user.id)

    def process_message(self, message):
        if message.from_user:
            self.insert_else_update_user(message.from_user)
