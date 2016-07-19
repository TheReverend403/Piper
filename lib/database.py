import lib.pickledb as pickledb


class Database(object):
    def __init__(self, path):
        self.db = pickledb.load(path, True)

    def get_user_value(self, user, key):
        return self.db.get(str(user.id) + ':' + key)

    def set_user_value(self, user, key, value):
        return self.db.set(str(user.id) + ':' + key, value)
