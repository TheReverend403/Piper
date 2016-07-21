import random
from lib.command import Command


class RollCommand(Command):
    name = 'roll'
    description = 'Roll some dice.'

    def run(self, message, args):
        if not args:
            self.reply(message, 'No roll specification supplied. Try */roll 3d6*.', parse_mode='Markdown')
            return

        spec = ''.join(char for char in ''.join(args) if char.isdigit() or char == 'd')
        dice_count, sep, dice_size = spec.partition('d')
        if not dice_count or not dice_size:
            self.reply(message, 'Invalid roll specification. Example: */roll 3d6*', parse_mode='Markdown')
            return

        dice_count = int(''.join(char for char in dice_count if char.isdigit()))
        dice_size = int(''.join(char for char in dice_size if char.isdigit()))
        if dice_count < 1 or dice_count > 64 or dice_size < 4 or dice_size > 128:
            self.reply(message, 'Invalid roll specification. Must be a minimum of *1d4* and a maximum of *64d128*',
                       parse_mode='Markdown')
            return

        rolls = [random.SystemRandom().randint(1, dice_size) for _ in range(dice_count)]
        self.reply(message, '[{0}] = {1}'.format(', '.join(map(str, rolls)), sum(rolls)))
