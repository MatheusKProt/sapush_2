import logging
import time
from functools import wraps
from uuid import uuid4

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import run_async

import crawlers
import dao
import db
import messages
import util

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
        telegram_id = update.effective_user.id
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
        telegram_id = update.effective_user.id
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
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    bot.send_message(chat_id=update['message']['chat']['id'], text=messages.termos(), parse_mode=ParseMode.HTML)


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
    elif query.data == 'configurar_notas':
        configurar_notas(bot, update, query)
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
        configurar_frequencia(bot, update, query)
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
    elif query.data == 'sair':
        bot.delete_message(chat_id=update['callback_query']['message']['chat']['id'],
                           message_id=query['message']['message_id'])
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
        bot.send_message(chat_id=telegram_id, text=messages.comandos(), parse_mode=ParseMode.HTML)
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


@registered
@restricted
@logged
def notas(bot, update):
    if int(time.strftime("%m", time.localtime())) >= 7:
        semestre = str(time.strftime("%Y/2", time.localtime()))
    else:
        semestre = str(time.strftime("%Y/1", time.localtime()))
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
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
    if int(time.strftime("%m", time.localtime())) >= 7:
        semestre = str(time.strftime("%Y/2", time.localtime()))
    else:
        semestre = str(time.strftime("%Y/1", time.localtime()))
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
    frequencia = session.query(db.Frequencia).filter_by(user_id=telegram_id, semestre=semestre)

    msg = "<b>Frequência</b>"
    for freq in frequencia:
        msg += "\n" + util.formata_frequencia(freq)
    bot.send_message(chat_id=telegram_id, text=msg, parse_mode=ParseMode.HTML)
    session.close()


@registered
@restricted
@logged
def horarios(bot, update):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=crawlers.get_horarios(user), parse_mode=ParseMode.HTML)
    session.close()


@registered
@restricted
@logged
def historico(bot, update):
    telegram_id = update['message']['chat']['id']
    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=messages.historico(crawlers.get_historico(user)),
                     parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    session.close()


@registered
@restricted
@logged
def disciplinas(bot, update):
    telegram_id = update['message']['chat']['id']
    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    disciplinas = crawlers.get_disciplinas(user)
    bot.send_message(chat_id=telegram_id, text=disciplinas, parse_mode=ParseMode.HTML)
    session.close()


@registered
@run_async
@restricted
@logged
def curriculo(bot, update):
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=crawlers.get_curriculo(user), parse_mode=ParseMode.HTML)
    session.close()


@registered
@restricted
@logged
def boleto(bot, update):
    telegram_id = update['message']['chat']['id']
    session = Session()
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
    session = Session()
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    bot.send_message(chat_id=telegram_id, text=messages.chave(user.chave[:-1]), parse_mode=ParseMode.HTML)
    session.close()


@registered
@restricted
@logged
def sugerir(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update['message']['chat']['id'],
                         text=messages.suggest_without_parameters(update['message']['chat']['first_name']),
                         parse_mode=ParseMode.HTML)
    else:
        session = Session()
        sugestao = db.Sugestoes(update['message']['chat']['id'], " ".join(args), time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
        session.add(sugestao)
        bot.send_message(chat_id=update['message']['chat']['id'], text=messages.sugestao(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)

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
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    bot.send_message(chat_id=update['message']['chat']['id'], text=messages.comandos(), parse_mode=ParseMode.HTML)


@registered
@restricted
def ajuda(bot, update):
    bot.send_message(chat_id=update['message']['chat']['id'],
                     text=messages.help_user(),
                     parse_mode=ParseMode.HTML)


@registered
@restricted
def callback(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    if "ajud" in str(update['message']['text']).lower() or "help" in str(update['message']['text']).lower():
        ajuda(bot, update)
    elif "notas" in str(update['message']['text']).lower():
        notas(bot, update)
    elif "frequencia" in str(update['message']['text']).lower():
        frequencia(bot, update)
    elif "horarios" in str(update['message']['text']).lower():
        horarios(bot, update)
    elif "disciplinas" in str(update['message']['text']).lower():
        disciplinas(bot, update)
    elif "historico" in str(update['message']['text']).lower():
        historico(bot, update)
    elif "curriculo" in str(update['message']['text']).lower():
        curriculo(bot, update)
    elif "boleto" in str(update['message']['text']).lower():
        boleto(bot, update)
    elif "chave" in str(update['message']['text']).lower():
        chave(bot, update)
    else:
        bot.send_message(chat_id=update['message']['chat']['id'],
                         text=messages.answer_error(format(update['message']['chat']['first_name'])),
                         parse_mode=ParseMode.HTML)


@registered
@restricted
def desenvolvedores(bot, update):
    bot.send_message(chat_id=update['message']['chat']['id'],
                     text=messages.developers(),
                     parse_mode=ParseMode.HTML)


@registered
@restricted
def editais(bot, update, args):
    try:
        bot.send_message(chat_id=update['message']['chat']['id'], text=crawlers.get_editais(int(args[0])),
                         parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except:
        bot.send_message(chat_id=update['message']['chat']['id'], text=crawlers.get_editais(5),
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
    keyboard = [[InlineKeyboardButton('Ativar', callback_data='notas_ativar'), InlineKeyboardButton('Desativar', callback_data='notas_desativar')],
                [InlineKeyboardButton('Sair', callback_data='sair')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                          message_id=query['message']['message_id'],
                          text=messages.configurar_notas(), reply_markup=reply_markup)


def configurar_frequencia(bot, update, query):
    keyboard = [[InlineKeyboardButton('Ativar', callback_data='frequencia_ativar'), InlineKeyboardButton('Desativar', callback_data='frequencia_desativar')],
                [InlineKeyboardButton('Sair', callback_data='sair')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=update['callback_query']['message']['chat']['id'],
                          message_id=query['message']['message_id'],
                          text=messages.configurar_frequencia(), reply_markup=reply_markup)


@registered
@restricted
def menu(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    keyboard = [[InlineKeyboardButton('Conta', callback_data='conta'), InlineKeyboardButton('Funções', callback_data='funcoes')],
                [InlineKeyboardButton('Sair', callback_data='sair')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update['message']['chat']['id'], text="<b>Menu</b>",
                     reply_markup=reply_markup, parse_mode=ParseMode.HTML)
