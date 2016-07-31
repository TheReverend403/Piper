import hashlib

from lib.command import Command


class HashCommand(Command):
    name = 'hash'
    description = 'Hashes text.'

    def run(self, message, args):
        # Remove duplicates
        available_algorithms = list(set(x.lower() for x in hashlib.algorithms_available))
        if not args or len(args) != 2:
            self.reply(message, '<b>/{0} [algorithm] [text]</b>, where [algorithm] is one of {1}'.format(
                self.name, ', '.join(available_algorithms)), parse_mode='HTML')
            return

        algorithm = args[0].lower()
        if algorithm not in [x for x in available_algorithms]:
            self.reply(message, 'Invalid algorithm. Please choose one of {0}'.format(
                ', '.join(available_algorithms)))
            return

        text = ' '.join(args[1:]).encode('utf-8')
        hash_object = hashlib.new(algorithm)
        hash_object.update(text)
        self.reply(message, hash_object.hexdigest())
