import logging
import random

import time
from time import sleep

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from gtables import Parser, MultipleQuestion
from threading import Thread

client = Parser("creds.json")
users_auth = []

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    for g in client.groups.values():
        if tg_user.name in g.users.keys():
            update.message.reply_text('Good afternoon, {}!\nYou are in `{}` group.'.format(g.users[tg_user.name].name, g.users[tg_user.name].group.name), parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
            if g.users[tg_user.name] not in users_auth:
                new_user = g.users[tg_user.name]
                new_user.tg_id = update.message.chat_id
                users_auth.append(new_user)
            break
    else:
        update.message.reply_text("You haven't enrolled to any *Kafedra* course.", parse_mode='Markdown',)


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('This bot can be used only for study on GoodLine Kafedra courses. Please ask your instructor to add your Telegram alias to participants list.')


def check_answer(update: Update, context: CallbackContext):
    for u in users_auth:
        if u.id == update.message.from_user.name:
            if u.q_now:
                if update.message.text == u.q_now.right_answer:
                    update.message.reply_text('Well done!')
                    u.answered[u.q_now] += 1
                    print(u.answered)
                else:
                    update.message.reply_text(u.q_now.theme.params['wrong_answer_pop'].format(answer=u.q_now.right_answer, site=u.q_now.theme.params['link']))
                u.q_now = None


def check_queue():
    while True:
        sleep(1)
        for u in users_auth:
            if u.queue:
                if not u.q_now:
                    question = u.queue.pop(0)
                    if isinstance(question, MultipleQuestion):
                        answers = question.remain_answers + [question.right_answer]
                        random.shuffle(answers)
                        answers = [[e] for e in answers]
                        updater.bot.send_message(u.tg_id, question.question_text, reply_markup=ReplyKeyboardMarkup(answers, one_time_keyboard=True))
                    else:
                        updater.bot.send_message(u.tg_id, question.question_text, reply_markup=ReplyKeyboardRemove())

                    u.q_now = question


updater = Updater("1497024833:AAGI9MWcP8ZTsVkNd0TnKEmBCub5LD3_Ahc", use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_answer))

updater.start_polling()

t = Thread(target=check_queue)
t.start()

while True:
    sleep(10)
    for g in client.groups.values():
        for t in g.themes:
            if int(t.params['repetitions_per_week']) < time.time():                   # TIME OF REPETITION PER WEEK
                for u in users_auth:
                    if t in u.group.themes:
                        ques = t.questions.copy()
                        for answered, kol in u.answered.items():
                            print(kol, answered.repetition)
                            if kol >= answered.repetition:
                                ques.remove(answered)
                        if ques:
                            chosen_question = random.choice(ques)
                            u.queue.append(chosen_question)
