from lib.command import Command


class IgnoreCommand(Command):
    name = 'ignore'
    description = 'Make me ignore all future commands from a user.'
    admin_only = True

    def run(self, message, args):
        if not message.reply_to_message or not message.reply_to_message.from_user:
            self.reply(message, 'Please send this command as a reply to a message from the user you wish to ignore.')
            return

        user = message.reply_to_message.from_user

        if user.id == message.from_user.id:
            self.reply(message, 'You cannot ask me to ignore yourself!')
            return

        if self.bot.is_admin(user):
            self.reply(message, 'I cannot ignore a bot admin!')
            return

        if self.bot.is_me(user):
            self.reply(message, 'I can\'t ignore myself, the voices won\'t let me.')
            return

        unignore = args and args[0] == '-u'
        if not unignore:
            self.bot.ignore(user)
        else:
            self.bot.unignore(user)

        self.reply(message, '{0} {1}!'.format('Ignored' if not unignore else 'Unignored', user.first_name))
