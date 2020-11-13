import logging

import time
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from gtables import Parser, User
from time import sleep

client = Parser("creds.json")
users_auth = []

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    tg_user = update.message.from_user
    for g in client.groups.values():
        print(g.users)
         # if tg_user.name not in g.users.keys() and g.users[tg_user.name] in users_auth:
         #     users_auth.discard(g.users[tg_user.name])
        if tg_user.name in g.users.keys():
            update.message.reply_text('Здравствуйте, {}! Вы принадлежите группе {}'.format(g.users[tg_user.name].name, g.users[tg_user.name].group.name))
            if g.users[tg_user.name] not in users_auth:
                new_user = g.users[tg_user.name]
                new_user.tg_id = update.message.chat_id
                users_auth.append(new_user)
            print(users_auth)
            break
    else:
        update.message.reply_text('Вы не зачислены ни на один курс.')



def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1497024833:AAGI9MWcP8ZTsVkNd0TnKEmBCub5LD3_Ahc", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    while True:
        sleep(5)
        print(users_auth)
        for g in client.groups.values():
            for t in g.themes:
                print(t.params)
                if int(t.params['repetitions_per_week']) < time.time():
                    for u in users_auth:
                        if t in u.group.themes:
                            print(u.tg_id)
                            updater.bot.send_message(u.tg_id, "hugij")
                    print("Time is up!")


if __name__ == '__main__':
    main()