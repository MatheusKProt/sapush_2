import logging
import time
from functools import wraps

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import run_async

import crawlers
import db
import messages

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

url = db.get_database_url()
engine = db.gen_engine(url)
Session = sessionmaker(bind=engine)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        telegram_id = update.effective_user.id
        session = Session()
        admin = session.query(db.User).filter_by(telegram_id=telegram_id, termos=True).first()
        if not admin:
            bot.send_message(chat_id=update['message']['chat']['id'],
                             text=messages.not_agreed(update['message']['chat']['first_name']),
                             parse_mode=ParseMode.HTML)
            session.close()
            return
        session.close()
        return func(bot, update, *args, **kwargs)

    return wrapped


def agreed(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        telegram_id = update.effective_user.id
        session = Session()
        user = session.query(db.User).filter_by(telegram_id=telegram_id, termos=True).first()
        if user:
            bot.send_message(chat_id=update['message']['chat']['id'],
                             text=messages.agreed(update['message']['chat']['first_name']),
                             parse_mode=ParseMode.HTML)
            session.close()
            return
        session.close()
        return func(bot, update, *args, **kwargs)

    return wrapped


@run_async
def start(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)  # Comando para o bot ficar digitando...
    telegram_id = update['message']['chat']['id']
    username = update['message']['chat']['username']
    first_name = update['message']['chat']['first_name']
    last_name = update['message']['chat']['last_name']
    data_criacao = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

    session = Session()
    try:
        user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
        if user:
            bot.send_message(chat_id=update['message']['chat']['id'],
                             text=messages.start(update['message']['chat']['first_name']),
                             parse_mode=ParseMode.HTML)
            if not user.termos:
                do_you_agree(bot, update)
            session.close()
            return
        user = db.User(telegram_id, username, first_name, last_name, "", "", False, True, True, data_criacao)
        session.add(user)

        session.commit()
        session.close()
    except():
        session.close()

    bot.send_message(chat_id=update['message']['chat']['id'],
                     text=messages.start(update['message']['chat']['first_name']),
                     parse_mode=ParseMode.HTML)
    do_you_agree(bot, update)


def termos(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    bot.send_message(chat_id=update['message']['chat']['id'], text=messages.termos(), parse_mode=ParseMode.HTML)


@agreed
def do_you_agree(bot, update):
    keyboard = [[InlineKeyboardButton('Aceitar', callback_data='1')],
                [InlineKeyboardButton('Recusar', callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages.do_you_agree(),
                     reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    telegram_id = query['message']['chat']['id']
    session = Session()
    try:
        user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
        if query.data == '1':
            termos = True
            bot.edit_message_text(text=messages.yes(query['message']['chat']['first_name']).format(query.data),
                                  chat_id=query['message']['chat']['id'],
                                  message_id=query['message']['message_id'])
            bot.send_message(chat_id=telegram_id, text=messages.login_requirement(), parse_mode=ParseMode.HTML)
        else:
            termos = False
            bot.edit_message_text(text=messages.no(query['message']['chat']['first_name']).format(query.data),
                                  chat_id=query['message']['chat']['id'],
                                  message_id=query['message']['message_id'])
        user.termos = termos
        session.commit()
        session.close()
    except():
        session.close()


@restricted
def login(bot, update, args):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)

    username = update['message']['chat']['username']
    first_name = update['message']['chat']['first_name']

    if len(args) != 2:
        bot.send_message(chat_id=telegram_id, text=messages.invalid_login(first_name), parse_mode=ParseMode.HTML)
        return

    sapu_username = args[0]
    sapu_password = args[1]

    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()

    s, logado, erro = crawlers.get_session(sapu_username, sapu_password)
    if logado:
        user.username = username
        user.first_name = first_name
        user.sapu_username = sapu_username
        user.sapu_password = sapu_password

        session.commit()
        session.close()

        bot.send_message(chat_id=telegram_id, text=messages.valid_login(first_name), parse_mode=ParseMode.HTML)
        bot.send_message(chat_id=telegram_id, text=messages.comandos(), parse_mode=ParseMode.HTML)
        return
    else:
        if erro == "senha":
            bot.send_message(chat_id=telegram_id, text=messages.wrong_password(first_name), parse_mode=ParseMode.HTML)
        elif erro == "usuario":
            bot.send_message(chat_id=telegram_id, text=messages.wrong_user(first_name), parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id=telegram_id, text=erro + ".", parse_mode=ParseMode.HTML)
        session.close()
        return


@restricted
def deletar(bot, update):
    telegram_id = update['message']['chat']['id']
    first_name = update['message']['chat']['first_name']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)

    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()

    if user.sapu_username == " ":
        bot.send_message(chat_id=telegram_id, text=messages.user_doesnt_exist(first_name), parse_mode=ParseMode.HTML)
        session.close()
        return

    user.sapu_username = " "
    user.sapu_password = " "

    session.commit()
    session.close()

    bot.send_message(chat_id=telegram_id, text=messages.user_deleted(first_name), parse_mode=ParseMode.HTML)
    return


@restricted
def comandos(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    bot.send_message(chat_id=update['message']['chat']['id'], text=messages.comandos(), parse_mode=ParseMode.HTML)
