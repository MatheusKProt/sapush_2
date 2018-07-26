import logging
import os
import time
from functools import wraps
from uuid import uuid4

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import run_async

import admins
import crawlers
import dao
import db
import messages
import util
import speech as sr

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

url = db.get_database_url()
engine = db.gen_engine(url)
Session = sessionmaker(bind=engine)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        telegram_id = update['message']['chat']['id']
        session = Session()
        user = session.query(db.User).filter_by(telegram_id=telegram_id, termos=True).first()
        if not user:
            bot.send_message(chat_id=update['message']['chat']['id'],
                             text=messages.not_agreed(update['message']['chat']['first_name']),
                             parse_mode=ParseMode.HTML)
            session.close()
            return
        session.close()
        return func(bot, update, *args, **kwargs)

    return wrapped


def logged(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        telegram_id = update['message']['chat']['id']
        session = Session()
        user = session.query(db.User).filter_by(telegram_id=telegram_id, termos=True).first()
        if user.sapu_username == " ":
            bot.send_message(chat_id=update['message']['chat']['id'],
                             text=messages.not_logged_in(update['message']['chat']['first_name']),
                             parse_mode=ParseMode.HTML)
            session.close()
            return
        session.close()
        return func(bot, update, *args, **kwargs)

    return wrapped


def registered(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        telegram_id = update['message']['chat']['id']
        session = Session()
        user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
        if not user:
            bot.send_message(chat_id=update['message']['chat']['id'],
                             text=messages.not_registered(update['message']['chat']['first_name']),
                             parse_mode=ParseMode.HTML)
            session.close()
            return
        session.close()
        return func(bot, update, *args, **kwargs)

    return wrapped


def agreed(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        telegram_id = update['message']['chat']['id']
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
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
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
        user = db.User(telegram_id, username, first_name, last_name, " ", " ", False, True, True, data_criacao, " ", " ")
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
    telegram_id = update['message']['chat']['id']
    usage(telegram_id, "Termos", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=telegram_id, text=messages.termos(), parse_mode=ParseMode.HTML)


@agreed
def do_you_agree(bot, update):
    keyboard = [[InlineKeyboardButton('Aceitar', callback_data='termos_aceitar'), InlineKeyboardButton('Recusar', callback_data='termos_recusar')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages.do_you_agree(),
                     reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    telegram_id = query['message']['chat']['id']
    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()

    # Termos
    if query.data == 'termos_aceitar':
        user.termos = True
        bot.edit_message_text(text=messages.yes().format(query.data),
                              chat_id=query['message']['chat']['id'],
                              message_id=query['message']['message_id'])
        bot.send_message(chat_id=telegram_id, text=messages.login_requirement(), parse_mode=ParseMode.HTML)
    elif query.data == 'termos_recusar':
        user.termos = False
        bot.edit_message_text(text=messages.no(query['message']['chat']['first_name']).format(query.data),
                              chat_id=query['message']['chat']['id'],
                              message_id=query['message']['message_id'])

    # Configurar
    elif query.data == 'configurar_notas':
        configurar_notas(bot, update['callback_query'], query)
    elif query.data == 'notas_ativar':
        user.push_notas = True
        bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                              message_id=query['message']['message_id'],
                              text=messages.configurar_notas_ativado(query['message']['chat']['first_name']))
    elif query.data == 'notas_desativar':
        user.push_notas = False
        bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                              message_id=query['message']['message_id'],
                              text=messages.configurar_notas_desativado(query['message']['chat']['first_name']))
    elif query.data == 'configurar_frequencia':
        configurar_frequencia(bot, update['callback_query'], query)
    elif query.data == 'frequencia_ativar':
        user.push_frequencia = True
        bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                              message_id=query['message']['message_id'],
                              text=messages.configurar_frequencia_ativado(query['message']['chat']['first_name']))
    elif query.data == 'frequencia_desativar':
        user.push_frequencia = False
        bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                              message_id=query['message']['message_id'],
                              text=messages.configurar_frequencia_desativado(query['message']['chat']['first_name']))

    # Deletar conta
    elif query.data == 'deletar_conta':
        deletar_conta(bot, update)
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
    elif query.data == 'nao_deletar_conta':
        bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'],
                              text=messages.not_delete_account(update['callback_query']['message']['chat']['first_name']), parse_mode=ParseMode.HTML)

    # Menu
    elif query.data == 'menu_perfil':
        menu_perfil(bot, update, query)
    elif query.data == 'menu_funcionalidades':
        menu_funcionalidades(bot, update, query)
    elif query.data == 'menu_outros':
        menu_outros(bot, update, query)
    elif query.data == 'voltar_menu':
        menu(bot, update['callback_query'], [query['message']['message_id']])

    # Perfil
    elif query.data == 'login':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        login(bot, update['callback_query'], [])
    elif query.data == 'deletar':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        deletar(bot, update['callback_query'])
    elif query.data == 'configurar':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        configurar(bot, update['callback_query'])

    # Funcionalidades
    elif query.data == 'notas':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        notas(bot, update['callback_query'])
    elif query.data == 'frequencia':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        frequencia(bot, update['callback_query'])
    elif query.data == 'horarios':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        horarios(bot, update['callback_query'])
    elif query.data == 'disciplinas':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        disciplinas(bot, update['callback_query'])
    elif query.data == 'historico':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        historico(bot, update['callback_query'])
    elif query.data == 'curriculo':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        curriculo(bot, update['callback_query'])
    elif query.data == 'boleto':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        boleto(bot, update['callback_query'])
    elif query.data == 'editais':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        editais(bot, update['callback_query'], [])
    elif query.data == 'chave':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        chave(bot, update['callback_query'])
    elif query.data == 'atestados':
        atestado(bot, update['callback_query'], query['message']['message_id'])
    elif query.data == 'moodle':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        moodle(bot, update['callback_query'])
    elif query.data == 'emails':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        emails(bot, update['callback_query'], [])

    # Outros
    elif query.data == 'desenvolvedores':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        desenvolvedores(bot, update['callback_query'])
    elif query.data == 'termos':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        termos(bot, update['callback_query'])
    elif query.data == 'ajuda':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        ajuda(bot, update['callback_query'])
    elif query.data == 'sugerir':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        sugerir(bot, update['callback_query'], [])
    elif query.data == 'comandos':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
        comandos(bot, update['callback_query'])

    # Users
    elif 'users_anterior' in query.data:
        admins.users_menu(bot, update['callback_query'], ["", "", query['message']['message_id'], int(str(query.data).split(" ")[1]) - 10, 1])
    elif 'users_proxima' in query.data:
        admins.users_menu(bot, update['callback_query'], ["", "", query['message']['message_id'], int(str(query.data).split(" ")[1]) + 10, 1])

    # Atestado
    elif 'atestado_simples' in query.data:
        atestado_simples(bot, update['callback_query'], query)
    elif 'atestado_completo' in query.data:
        atestado_completo(bot, update['callback_query'], query)
    elif 'atestado_apto' in query.data:
        atestado_apto(bot, update['callback_query'], query)

    # Geral
    elif query.data == 'sair':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'], message_id=query['message']['message_id'])
    else:
        bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                              message_id=query['message']['message_id'],
                              text="No futuro vai abrir a função!")
    session.commit()
    session.close()


@registered
@restricted
def login(bot, update, args):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Login", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))

    username = update['message']['chat']['username']
    first_name = update['message']['chat']['first_name']

    if len(args) != 2:
        bot.send_message(chat_id=telegram_id, text=messages.invalid_login(first_name), parse_mode=ParseMode.HTML)
        return

    sapu_username = args[0]
    sapu_password = args[1]

    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()

    _, logado, error, chave, curso = crawlers.get_session(sapu_username, sapu_password)
    if logado:
        user.username = username
        user.first_name = first_name
        user.sapu_username = sapu_username
        user.sapu_password = sapu_password
        user.chave = chave
        user.curso = curso

        session.commit()

        user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
        notas_resumo, notas_detalhe = crawlers.get_notas(user)
        frequencia = crawlers.get_frequencia(user)

        dao.set_notas(user, notas_resumo, notas_detalhe)
        dao.set_frequencia(user, frequencia)
        session.close()

        bot.send_message(chat_id=telegram_id, text=messages.valid_login(first_name), parse_mode=ParseMode.HTML)
        menu(bot, update, [])
        return
    else:
        if error == "senha":
            bot.send_message(chat_id=telegram_id, text=messages.wrong_password(first_name), parse_mode=ParseMode.HTML)
        elif error == "usuario":
            bot.send_message(chat_id=telegram_id, text=messages.wrong_user(first_name), parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id=telegram_id, text=error + ".", parse_mode=ParseMode.HTML)
        session.close()
        return


@registered
@restricted
def deletar(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    keyboard = [[InlineKeyboardButton('Sim', callback_data='deletar_conta'), InlineKeyboardButton('Não', callback_data='nao_deletar_conta')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update['message']['chat']['id'], text=messages.delete_user(update['message']['chat']['first_name']),
                     reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def deletar_conta(bot, update):
    telegram_id = update['callback_query']['message']['chat']['id']
    first_name = update['callback_query']['message']['chat']['first_name']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Deletar", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))

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


@registered
@restricted
@logged
def notas(bot, update):
    session = Session()
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Notas", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    if int(time.strftime("%m", time.localtime())) >= 7:
        semestre = str(time.strftime("%Y/2", time.localtime()))
    else:
        semestre = str(time.strftime("%Y/1", time.localtime()))
    notas_resumo = session.query(db.NotasResumo).filter_by(user_id=telegram_id, semestre=semestre)

    if notas_resumo.first():
        msg = "<b>Notas</b>"
        for resumo in notas_resumo:
            msg += "\n" + util.formata_notas_resumo(resumo)
    else:
        msg = messages.notas_empty(update['message']['chat']['first_name'])
    bot.send_message(chat_id=telegram_id, text=msg, parse_mode=ParseMode.HTML)
    session.close()


@registered
@restricted
@logged
def frequencia(bot, update):
    session = Session()
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Frequência", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    if int(time.strftime("%m", time.localtime())) >= 7:
        semestre = str(time.strftime("%Y/2", time.localtime()))
    else:
        semestre = str(time.strftime("%Y/1", time.localtime()))
    frequencia = session.query(db.Frequencia).filter_by(user_id=telegram_id, semestre=semestre)
    if frequencia.first():
        msg = "<b>Frequência</b>"
        for freq in frequencia:
            msg += "\n" + util.formata_frequencia(freq)
    else:
        msg = messages.frequencia_empty(update['message']['chat']['first_name'])
    bot.send_message(chat_id=telegram_id, text=msg, parse_mode=ParseMode.HTML)
    session.close()


@registered
@restricted
@logged
def horarios(bot, update):
    session = Session()
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Horários", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=crawlers.get_horarios(user), parse_mode=ParseMode.HTML)
    session.close()


@registered
@restricted
@logged
def historico(bot, update):
    session = Session()
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Histórico", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=messages.historico(crawlers.get_historico(user)),
                     parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    session.close()


@registered
@restricted
@logged
def disciplinas(bot, update):
    session = Session()
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Disciplinas", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    disciplinas = crawlers.get_disciplinas(user)
    bot.send_message(chat_id=telegram_id, text=disciplinas, parse_mode=ParseMode.HTML)
    session.close()


@registered
@run_async
@restricted
@logged
def curriculo(bot, update):
    session = Session()
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Currículo", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=crawlers.get_curriculo(user), parse_mode=ParseMode.HTML)
    session.close()


@registered
@run_async
@restricted
@logged
def atestado(bot, update, *args):
    if args:
        keyboard = [[InlineKeyboardButton('Simples', callback_data='atestado_simples'), InlineKeyboardButton('Completo', callback_data='atestado_completo')],
                    [InlineKeyboardButton('Apto', callback_data='atestado_apto'), InlineKeyboardButton('Voltar', callback_data='menu_funcionalidades')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id=update['message']['chat']['id'], message_id=args[0], text=messages.atestado(),
                              reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        keyboard = [[InlineKeyboardButton('Simples', callback_data='atestado_simples'), InlineKeyboardButton('Completo', callback_data='atestado_completo')],
                    [InlineKeyboardButton('Apto', callback_data='atestado_apto'), InlineKeyboardButton('Sair', callback_data='sair')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=update['message']['chat']['id'], text=messages.atestado(), reply_markup=reply_markup)


def atestado_simples(bot, update, query):
    telegram_id = update['message']['chat']['id']
    session = Session()
    usage(telegram_id, "Atestado simples", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    atestado = crawlers.get_atestado_simples(user)
    bot.edit_message_text(chat_id=update['message']['chat']['id'],
                          message_id=query['message']['message_id'],
                          text=messages.formata_atestado("simples ", atestado), parse_mode=ParseMode.HTML,
                          disable_web_page_preview=True)
    session.close()


def atestado_completo(bot, update, query):
    telegram_id = update['message']['chat']['id']
    session = Session()
    usage(telegram_id, "Atestado completo", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    atestado = crawlers.get_atestado_completo(user)
    bot.edit_message_text(chat_id=update['message']['chat']['id'],
                          message_id=query['message']['message_id'],
                          text=messages.formata_atestado("completo ", atestado), parse_mode=ParseMode.HTML,
                          disable_web_page_preview=True)
    session.close()


def atestado_apto(bot, update, query):
    telegram_id = update['message']['chat']['id']
    session = Session()
    usage(telegram_id, "Atestado apto", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    atestado = crawlers.get_atestado_apto(user)
    bot.edit_message_text(chat_id=update['message']['chat']['id'],
                          message_id=query['message']['message_id'],
                          text=messages.formata_atestado("", atestado), parse_mode=ParseMode.HTML,
                          disable_web_page_preview=True)
    session.close()


@registered
@restricted
@logged
def boleto(bot, update):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
    usage(telegram_id, "Boleto", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    boleto, status = crawlers.get_boleto(user)
    if status:
        bot.send_message(chat_id=telegram_id, text=messages.boleto(user.first_name, boleto, 1),
                         parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        bot.send_message(chat_id=telegram_id, text=messages.boleto(user.first_name, boleto, 2),
                         parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    session.close()


@registered
@restricted
@logged
def chave(bot, update):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
    usage(telegram_id, "Chave", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=messages.chave(user.chave[:-1]), parse_mode=ParseMode.HTML)
    session.close()


@registered
@run_async
@restricted
@logged
def moodle(bot, update):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
    usage(telegram_id, "Moodle", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=messages.formata_moodle(crawlers.get_moodle(user)), parse_mode=ParseMode.HTML)
    session.close()


@registered
@run_async
@restricted
@logged
def emails(bot, update, args):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
    usage(telegram_id, "Emails", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=crawlers.get_emails(user, args), parse_mode=ParseMode.HTML)
    session.close()


@registered
@restricted
@logged
def sugerir(bot, update, args):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
    usage(telegram_id, "Sugerir", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    if len(args) == 0:
        bot.send_message(chat_id=telegram_id,
                         text=messages.suggest_without_parameters(update['message']['chat']['first_name']),
                         parse_mode=ParseMode.HTML)
    else:
        sugestao = db.Sugestoes(telegram_id, " ".join(args), time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
        session.add(sugestao)
        bot.send_message(chat_id=telegram_id, text=messages.sugestao(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)

        session.commit()
    session.close()


def inlinequery(bot, update):
    if int(time.strftime("%m", time.localtime())) >= 7:
        semestre = str(time.strftime("%Y/2", time.localtime()))
    else:
        semestre = str(time.strftime("%Y/1", time.localtime()))
    results = list()
    session = Session()
    users = session.query(db.User)
    session.close()
    results.append(InlineQueryResultArticle(id=uuid4(), title="Erro",
                                            description="Você não efetuou o login.",
                                            input_message_content=InputTextMessageContent("Você não efetuou o login.",
                                                                                          parse_mode=ParseMode.HTML)))
    for user in users:
        if str(user.telegram_id) in str(update) and user.sapu_username != " ":
            results.pop(0)
            results.append(InlineQueryResultArticle(id=uuid4(), title="Notas",
                                                    description="Retorna suas notas do semestre atual.",
                                                    input_message_content=InputTextMessageContent(notas_inline(user, semestre),
                                                                                                  parse_mode=ParseMode.HTML)))
            results.append(InlineQueryResultArticle(id=uuid4(), title="Frequência",
                                                    description="Retorna sua frequência do semestre atual.",
                                                    input_message_content=InputTextMessageContent(frequencia_inline(user, semestre),
                                                                                                  parse_mode=ParseMode.HTML)))
            results.append(InlineQueryResultArticle(id=uuid4(), title="Horarios",
                                                    description="Retorna seus horários do semestre atual.",
                                                    input_message_content=InputTextMessageContent(horarios_inline(user),
                                                                                                  parse_mode=ParseMode.HTML)))
    update.inline_query.answer(results, is_personal=True, cache_time=0)


def notas_inline(user, semestre):
    session = Session()
    notas_resumo = session.query(db.NotasResumo).filter_by(user_id=user.telegram_id, semestre=semestre)
    session.close()
    if notas_resumo.first():
        notas = "<b>Notas</b>"
        for resumo in notas_resumo:
            notas += "\n" + util.formata_notas_resumo(resumo)
    else:
        notas = messages.notas_empty(user.first_name)
    return notas


def frequencia_inline(user, semestre):
    session = Session()
    frequencia_db = session.query(db.Frequencia).filter_by(user_id=user.telegram_id, semestre=semestre)
    frequencia = "<b>Frequência</b>\n"
    for freq in frequencia_db:
        frequencia += util.formata_frequencia(freq) + "\n"
    session.close()
    return frequencia


def horarios_inline(user):
    return crawlers.get_horarios(user)


@registered
@restricted
def comandos(bot, update):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Comandos", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=telegram_id, text=messages.comandos(), parse_mode=ParseMode.HTML)


@registered
@restricted
def ajuda(bot, update):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Ajuda", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    bot.send_message(chat_id=telegram_id, text=messages.help_user(), parse_mode=ParseMode.HTML)


@registered
@restricted
def callback(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    verifica_callback(bot, update, str(update['message']['text']).lower())


def verifica_callback(bot, update, arg):
    if "ajud" in arg or "help" in arg:
        ajuda(bot, update)
    elif "nota" in arg:
        notas(bot, update)
    elif "frequencia" in arg or "frequência" in arg:
        frequencia(bot, update)
    elif "horario" in arg or "horário" in arg:
        horarios(bot, update)
    elif "disciplina" in arg:
        disciplinas(bot, update)
    elif "historico" in arg or "histórico" in arg:
        historico(bot, update)
    elif "curriculo" in arg or "currículo" in arg:
        curriculo(bot, update)
    elif "boleto" in arg:
        boleto(bot, update)
    elif "chave" in arg:
        chave(bot, update)
    elif "comando" in arg:
        comandos(bot, update)
    elif "termo" in arg:
        termos(bot, update)
    elif "desenvolvedor" in arg or "desenvolveu" in arg:
        desenvolvedores(bot, update)
    elif "editais" in arg or "edital" in arg:
        args = []
        text = str(update['message']['text']).split(" ")
        if text[0].lower() == "editais":
            if len(text) == 2:
                args = [text[1]]
        editais(bot, update, args)
    elif "configura" in arg:
        configurar(bot, update)
    elif "start" in arg:
        start(bot, update)
    elif "login" in arg:
        args = []
        text = str(update['message']['text']).split(" ")
        if text[0].lower() == "login":
            if len(text) == 3:
                args = [text[1], text[2]]
        login(bot, update, args)
    elif "delet" in arg:
        deletar(bot, update)
    elif "sugerir" in arg or "sugiro" in arg or "sugest" in arg:
        args = []
        text = str(update['message']['text']).split(" ")
        if text[0].lower() == "sugerir":
            text.pop(0)
            args = text
        sugerir(bot, update, args)
    elif "menu" in arg:
        menu(bot, update, [])
    elif "atestado" in arg:
        atestado(bot, update)
    elif "moodle" in arg:
        moodle(bot, update)
    elif "email" in arg or "e-mail" in arg:
        emails(bot, update, [])
    else:
        bot.send_message(chat_id=update['message']['chat']['id'],
                         text=messages.answer_error(format(update['message']['chat']['first_name'])),
                         parse_mode=ParseMode.HTML)


@registered
@restricted
def desenvolvedores(bot, update):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Desenvolvedores", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    bot.send_message(chat_id=telegram_id, text=messages.developers(),
                     parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@registered
@restricted
def editais(bot, update, args):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    usage(telegram_id, "Editais", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    try:
        bot.send_message(chat_id=telegram_id, text=crawlers.get_editais(int(args[0])),
                         parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except:
        bot.send_message(chat_id=telegram_id, text=crawlers.get_editais(5),
                         parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@registered
@restricted
def configurar(bot, update):
    keyboard = [[InlineKeyboardButton('Notas', callback_data='configurar_notas'), InlineKeyboardButton('Frequência', callback_data='configurar_frequencia')],
                [InlineKeyboardButton('Sair', callback_data='sair')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update['message']['chat']['id'],
                     text=messages.configurar(),
                     reply_markup=reply_markup)


def configurar_notas(bot, update, query):
    telegram_id = update['message']['chat']['id']
    usage(telegram_id, "Configurar notas", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    keyboard = [[InlineKeyboardButton('Ativar', callback_data='notas_ativar'), InlineKeyboardButton('Desativar', callback_data='notas_desativar')],
                [InlineKeyboardButton('Sair', callback_data='sair')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=telegram_id, message_id=query['message']['message_id'],
                          text=messages.configurar_notas(), reply_markup=reply_markup)


def configurar_frequencia(bot, update, query):
    telegram_id = update['message']['chat']['id']
    usage(telegram_id, "Configurar frequência", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    keyboard = [[InlineKeyboardButton('Ativar', callback_data='frequencia_ativar'), InlineKeyboardButton('Desativar', callback_data='frequencia_desativar')],
                [InlineKeyboardButton('Sair', callback_data='sair')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=telegram_id, message_id=query['message']['message_id'],
                          text=messages.configurar_frequencia(), reply_markup=reply_markup)


@registered
@restricted
@run_async
def menu(bot, update, args):
    telegram_id = update['message']['chat']['id']
    usage(telegram_id, "Menu", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    keyboard = [[InlineKeyboardButton('Perfil', callback_data='menu_perfil'), InlineKeyboardButton('Funcionalidades', callback_data='menu_funcionalidades')],
                [InlineKeyboardButton('Outros', callback_data='menu_outros'), InlineKeyboardButton('Sair', callback_data='sair')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if len(args) == 0:
        bot.send_message(chat_id=telegram_id, text="<b>Menu</b>",
                         reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        bot.edit_message_text(chat_id=telegram_id,
                              message_id=args[0],
                              text="<b>Menu</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def menu_perfil(bot, update, query):
    keyboard = [[InlineKeyboardButton('Login', callback_data='login'), InlineKeyboardButton('Deletar', callback_data='deletar')],
                [InlineKeyboardButton('Configurar', callback_data='configurar'), InlineKeyboardButton('Voltar', callback_data='voltar_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                          message_id=query['message']['message_id'],
                          text="<b>Menu</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def menu_funcionalidades(bot, update, query):
    keyboard = [[InlineKeyboardButton('Notas', callback_data='notas'), InlineKeyboardButton('Frequência', callback_data='frequencia')],
                [InlineKeyboardButton('Horários', callback_data='horarios'), InlineKeyboardButton('Disciplinas', callback_data='disciplinas')],
                [InlineKeyboardButton('Histórico', callback_data='historico'), InlineKeyboardButton('Curriculo', callback_data='curriculo')],
                [InlineKeyboardButton('Boleto', callback_data='boleto'), InlineKeyboardButton('Editais', callback_data='editais')],
                [InlineKeyboardButton('Chave', callback_data='chave'), InlineKeyboardButton('Atestados', callback_data='atestados')],
                [InlineKeyboardButton('Moodle', callback_data='moodle'), InlineKeyboardButton('Emails', callback_data='emails')],
                [InlineKeyboardButton('Voltar', callback_data='voltar_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                          message_id=query['message']['message_id'],
                          text="<b>Menu</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def menu_outros(bot, update, query):
    keyboard = [[InlineKeyboardButton('Desenvolvedores', callback_data='desenvolvedores'), InlineKeyboardButton('Termos', callback_data='termos')],
                [InlineKeyboardButton('Ajuda', callback_data='ajuda'), InlineKeyboardButton('Sugerir', callback_data='sugerir')],
                [InlineKeyboardButton('Comandos', callback_data='comandos'), InlineKeyboardButton('Voltar', callback_data='voltar_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                          message_id=query['message']['message_id'],
                          text="<b>Menu</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)


@run_async
def usage(telegram_id, funcionabilidade, data):
    session = Session()
    session.add(db.Usage(telegram_id, funcionabilidade, data))
    session.commit()
    session.close()


@registered
@run_async
@restricted
@logged
def voice_to_text(bot, update):
    telegram_id = update['message']['chat']['id']
    usage(telegram_id, "Audio", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    first_name = update['message']['chat']['first_name']
    file_name = '/home/pi/SAPU/audios/' + str(telegram_id) + '_' + str(update.message.from_user.id) + str(update.message.message_id) + '.ogg'

    update.message.voice.get_file().download(file_name)

    BING_KEY = "07021ed50fb04b89bacf60c4eec35e51"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
    try:
        message_text = sr.recognize_bing(file_name, key=BING_KEY, language="pt-BR")
        success = True
    except sr.UnknownValueError:
        message_text = messages.speech_error(first_name)
        success = False
    except sr.RequestError:
        message_text = messages.speech_request_error(first_name)
        success = False
    os.remove(file_name)

    if success:
        verifica_callback(bot, update, str(message_text).lower())
    else:
        bot.send_message(chat_id=telegram_id, text=message_text, parse_mode=ParseMode.HTML)
