import time
import subprocess
import operator
from functools import wraps

import psutil
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from telegram import ParseMode, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import run_async

import db
import main
import messages
import util

url = db.get_database_url()
engine = db.gen_engine(url)
Session = sessionmaker(bind=engine)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update['message']['chat']['id']
        session = Session()
        admin = session.query(db.Admins).filter_by(user_id=user_id).first()
        if not admin:
            bot.send_message(chat_id=update['message']['chat']['id'],
                             text=messages.not_allowed(update['message']['chat']['first_name']),
                             parse_mode=ParseMode.HTML)
            session.close()
            return
        session.close()
        return func(bot, update, *args, **kwargs)

    return wrapped


def start(bot):
    session = Session()
    admins = session.query(db.Admins)
    for admin in admins:
        bot.send_message(chat_id=admin.user_id,
                         text=messages.start_server(),
                         parse_mode=ParseMode.HTML)


@restricted
@run_async
def users(bot, update, args):
    session = Session()
    users = session.query(db.User).order_by(db.User.first_name.asc(), db.User.last_name.asc())
    session.close()
    if not args:
        users_menu(bot, update, args)
    elif len(args) == 1:
        if str(args[0]).lower() == "count":
            usuarios = messages.count_users(update['message']['chat']['first_name'], users.count())
            bot.send_message(chat_id=update['message']['chat']['id'], text=usuarios, parse_mode=ParseMode.HTML)
        else:
            users_menu(bot, update, [args[0], "", -1, 0, 2])
    elif len(args) == 2:
        users_menu(bot, update, [args[0], args[1], -1, 0, 3])
    else:
        bot.send_message(chat_id=update['message']['chat']['id'],
                         text=messages.usuario_nao_encontrado(update['message']['chat']['first_name']),
                         parse_mode=ParseMode.HTML)


@restricted
@run_async
def suggestions(bot, update, args):
    session = Session()
    text = "<b>Sugestões</b>\n"
    if len(args) == 0:
        sugestoes = session.query(db.Sugestoes).order_by(db.Sugestoes.id.desc()).limit(10)
        sug = False
        for sugestao in sugestoes:
            user = session.query(db.User).filter_by(telegram_id=sugestao.user_id).first()
            text += messages.formata_sugestoes(user.first_name, user.last_name, sugestao.sugestao)
            sug = True
        if not sug:
            text += messages.no_suggestions()
        bot.send_message(chat_id=update['message']['chat']['id'], text=text, parse_mode=ParseMode.HTML)
    elif len(args) == 1:
        sug = False
        try:
            if int(args[0]) == 0:
                sugestoes = session.query(db.Sugestoes).order_by(db.Sugestoes.id.desc()).limit(10)
            else:
                sugestoes = session.query(db.Sugestoes).order_by(db.Sugestoes.id.desc()).limit(int(args[0]))
        except ValueError:
            sugestoes = session.query(db.Sugestoes).order_by(db.Sugestoes.id.desc()).limit(10)
        for sugestao in sugestoes:
            user = session.query(db.User).filter_by(telegram_id=sugestao.user_id).first()
            text += messages.formata_sugestoes(user.first_name, user.last_name, sugestao.sugestao)
            sug = True
        if not sug:
            text += messages.no_suggestions()
        bot.send_message(chat_id=update['message']['chat']['id'], text=text, parse_mode=ParseMode.HTML)
    session.close()


@restricted
@run_async
def push(bot, update, args):
    quantidade = 5
    if len(args) == 2:
        try:
            quantidade = int(args[1])
        except ValueError:
            pass
    elif len(args) == 1:
        try:
            quantidade = int(args[0])
        except ValueError:
            pass
    session = Session()
    notas = session.query(db.PushNotas).order_by(db.PushNotas.id.desc()).limit(quantidade)
    frequencia = session.query(db.PushFrequencia).order_by(db.PushFrequencia.id.desc()).limit(quantidade)
    msg = "<b>Push</b>\n"
    if len(args) == 0:
        msg += "\n<b>Notas</b>"
        msg += util.push(notas)
        msg += "\n\n<b>Frequência</b>"
        msg += util.push(frequencia)
        bot.send_message(chat_id=update['message']['chat']['id'], text=msg, parse_mode=ParseMode.HTML)
    elif "nota" in str(args[0]).lower():
        msg += "\n<b>Notas</b>"
        msg += util.push(notas)
        bot.send_message(chat_id=update['message']['chat']['id'], text=msg, parse_mode=ParseMode.HTML)
    elif "frequencia" in str(args[0]).lower():
        msg += "\n<b>Frequência</b>"
        msg += util.push(frequencia)
        bot.send_message(chat_id=update['message']['chat']['id'], text=msg, parse_mode=ParseMode.HTML)
    else:
        msg += "\n<b>Notas</b>"
        msg += util.push(notas)
        msg += "\n\n<b>Frequência</b>"
        msg += util.push(frequencia)
        bot.send_message(chat_id=update['message']['chat']['id'], text=msg, parse_mode=ParseMode.HTML)
    session.close()


@restricted
@run_async
def message(bot, update, args):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    msg = ""
    count = 0
    if len(args) == 0:
        bot.send_message(chat_id=update['message']['chat']['id'],
                         text=messages.alert_error(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)
        return
    for i in args:
        if count != 0:
            i = str(i).replace("\\n", '\n')
            msg += i + " "
        count += 1
    try:
        if int(args[0]):
            session = Session()
            user = session.query(db.User).filter_by(telegram_id=int(args[0])).first()
            bot.send_message(chat_id=args[0], text=messages.message(msg, update['message']['chat']['first_name'], user.first_name), parse_mode=ParseMode.HTML)
            admin = session.query(db.Admins).filter_by(user_id=update['message']['chat']['id']).first()
            session.add(db.Alert(admin.id, int(args[0]), str(msg)))
            user = session.query(db.User).filter_by(telegram_id=admin.user_id).first()
            bot.send_message(chat_id=update['message']['chat']['id'], text=messages.alert_success(user.first_name), parse_mode=ParseMode.HTML)

            session.commit()
            session.close()
    except ValueError:
        bot.send_message(chat_id=update['message']['chat']['id'], text=messages.alert_error(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)
    except Exception as error:
        main.error_callback(bot, update, error)


@restricted
@run_async
def breakdown(bot, update, args):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    msg = ""
    count = 0
    if len(args) == 0:
        bot.send_message(chat_id=update['message']['chat']['id'],
                         text=messages.alert_error(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)
        return
    for i in args:
        if count != 0:
            i = str(i).replace("\\n", '\n')
            msg += i + " "
        count += 1
    try:
        if int(args[0]):
            bot.send_message(chat_id=args[0], text=messages.alert(msg), parse_mode=ParseMode.HTML)
            bot.send_message(chat_id=update['message']['chat']['id'], text=messages.alert_success(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)
    except ValueError:
        bot.send_message(chat_id=update['message']['chat']['id'], text=messages.alert_error(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)
    except Exception as error:
        main.error_callback(bot, update, error)


@restricted
@run_async
def alert(bot, update, args):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    msg = ""
    if len(args) == 0:
        bot.send_message(chat_id=update['message']['chat']['id'],
                         text=messages.statement_error(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)
        return
    for i in args:
        i = str(i).replace("\\n", '\n')
        msg += i + " "
    session = Session()
    users = session.query(db.User)
    for u in users:
        bot.send_message(chat_id=u.telegram_id, text=messages.alert(msg), parse_mode=ParseMode.HTML)
    admin = session.query(db.Admins).filter_by(user_id=update['message']['chat']['id']).first()
    session.add(db.Statement(admin.id, str(msg)))
    session.commit()
    session.close()


@restricted
@run_async
def statistics(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    tempo_ligado = time.time() - psutil.boot_time()
    dias_ligado = int(tempo_ligado / 24 / 60 / 60)
    horas_ligado = int(tempo_ligado / 60 / 60 % 24)
    minutos_ligado = int(tempo_ligado / 60 % 60)
    segundos_ligado = int(tempo_ligado % 60)
    processador = psutil.cpu_percent()
    memoria = psutil.virtual_memory()
    disco = psutil.disk_usage('/')

    pids = psutil.pids()
    processos_consumindo = ''
    processos = {}

    for pid in pids:
        processo = psutil.Process(pid)
        try:
            memoria_processo = processo.memory_percent()
            if memoria_processo > 0.5:
                if processo.name() in processos:
                    processos[processo.name()] += memoria_processo
                else:
                    processos[processo.name()] = memoria_processo
        except():
            bot.send_message(chat_id=update['message']['chat']['id'], text="Erro", parse_mode=ParseMode.HTML)
    ordenar_processos = sorted(processos.items(), key=operator.itemgetter(1), reverse=True)
    for proc in ordenar_processos:
        processos_consumindo += """
{}, usando {}% de memória""".format(proc[0], round(proc[1]), 2)

    ligado = "Ligado há %d dias, %d horas, %d minutos e %d segundos" % (dias_ligado, horas_ligado, minutos_ligado, segundos_ligado)
    memoria_total = memoria.total / 1000000000
    memoria_disponivel = memoria.available / 1000000000
    memoria_usada = memoria_total - memoria_disponivel
    disco_total = disco.total / 1073741824
    disco_usado = disco.used / 1073741824
    disco_disponivel = disco.free / 1073741824

    bot.send_message(chat_id=update['message']['chat']['id'],
                     text=messages.statistics(ligado, processador, memoria.percent, disco.percent, memoria_total,
                                              memoria_usada, memoria_disponivel, disco_total, disco_usado, disco_disponivel,
                                              processos_consumindo),
                     parse_mode=ParseMode.HTML)


@restricted
@run_async
def usage(bot, update, args):
    session = Session()
    telegram_id = update['message']['chat']['id']
    bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
    try:
        if str(args[0]).lower() == "all":
            try:
                limite = int(args[1])
            except:
                limite = 10
            usages = session.query(db.Usage).order_by(db.Usage.id.desc()).limit(limite)
            msg = "<b>Histórico</b>\n"
            for usage in usages:
                user = session.query(db.User).filter_by(telegram_id=usage.user_id).first()
                msg += messages.formata_usage(usage.funcionabilidade + " | " + user.first_name + " " + user.last_name, usage.data[:-3])
            bot.send_message(chat_id=telegram_id, text=msg, parse_mode=ParseMode.HTML)
        else:
            try:
                limite = int(args[1])
            except:
                limite = 5
            usages = session.query(db.Usage).filter_by(user_id=int(args[0])).order_by(db.Usage.data.desc()).limit(limite)
            user = session.query(db.User.first_name, db.User.last_name).filter_by(telegram_id=int(args[0])).first()
            msg = "<b>Histórico de {} {}</b>\n".format(user[0], user[1])
            for usage in usages:
                msg += messages.formata_usage(usage.funcionabilidade, usage.data[:-3])
            bot.send_message(chat_id=telegram_id, text=msg, parse_mode=ParseMode.HTML)
        session.close()
    except:
        usages = session.query(db.Usage.funcionabilidade, func.count(db.Usage.funcionabilidade)).group_by(db.Usage.funcionabilidade).order_by(func.count(db.Usage.funcionabilidade).desc(), db.Usage.funcionabilidade.asc()).all()
        msg = "<b>Histórico</b>\n"
        for usage in usages:
            msg += messages.formata_usage(usage[0], usage[1])
        bot.send_message(chat_id=telegram_id, text=msg, parse_mode=ParseMode.HTML)
        session.close()


@restricted
def reboot(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    bot.send_message(chat_id=update['message']['chat']['id'], text="O servidor está reiniciando...",
                     parse_mode=ParseMode.HTML)
    subprocess.call(["sudo", "reboot", "now"])


@restricted
@run_async
def commands(bot, update):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)
    bot.send_message(chat_id=update['message']['chat']['id'], text=messages.comandos_admin(), parse_mode=ParseMode.HTML)


@restricted
@run_async
def errors(bot, update, args):
    session = Session()
    text = "<b>Erros</b>\n"
    if len(args) == 0:
        errors = session.query(db.Error).order_by(db.Error.id.desc()).limit(10)
        sug = False
        for error in errors:
            text += messages.formata_error(error.erro, error.data)
            sug = True
        if not sug:
            text += messages.no_error()
        bot.send_message(chat_id=update['message']['chat']['id'], text=text, parse_mode=ParseMode.HTML)
    elif len(args) == 1:
        sug = False
        try:
            if int(args[0]) == 0:
                errors = session.query(db.Error).order_by(db.Error.id.desc()).limit(10)
            else:
                errors = session.query(db.Error).order_by(db.Error.id.desc()).limit(int(args[0]))
        except ValueError:
            errors = session.query(db.Error).order_by(db.Error.id.desc()).limit(10)
        for error in errors:
            text += messages.formata_error(error.erro, error.data)
            sug = True
        if not sug:
            text += messages.no_error()
        bot.send_message(chat_id=update['message']['chat']['id'], text=text, parse_mode=ParseMode.HTML)
    session.close()


@restricted
@run_async
def users_menu(bot, update, args):
    telegram_id = update['message']['chat']['id']
    session = Session()
    usuarios = "<b>Usuários</b>\n"
    if not args:
        users = session.query(db.User).order_by(db.User.first_name.asc(), db.User.last_name.asc())
    elif args[4] == 1:
        users = session.query(db.User).order_by(db.User.first_name.asc(), db.User.last_name.asc())
    elif args[4] == 2:
        users = session.query(db.User).filter(db.User.first_name.like('%' + args[0] + '%')).order_by(db.User.first_name.asc(), db.User.last_name.asc()).from_self()
        if not users.first():
            users = session.query(db.User).filter(db.User.first_name.like('%' + args[0].capitalize() + '%')).order_by(db.User.first_name.asc(), db.User.last_name.asc()).from_self()
            if not users.first():
                bot.send_message(chat_id=update['message']['chat']['id'],
                                 text=messages.usuario_nao_encontrado(update['message']['chat']['first_name']),
                                 parse_mode=ParseMode.HTML)
                return
    elif args[4] == 3:
        users = session.query(db.User).filter(db.User.first_name.like('%' + args[0] + '%'),
                                              db.User.last_name.like('%' + args[1] + '%')).order_by(db.User.first_name.asc(), db.User.last_name.asc()).from_self()
        if not users.first():
            users = session.query(db.User).filter(db.User.first_name.like('%' + args[0].capitalize() + '%'),
                                                  db.User.last_name.like('%' + args[1].capitalize() + '%')).order_by(db.User.first_name.asc(), db.User.last_name.asc()).from_self()
            if not users.first():
                users = session.query(db.User).filter(db.User.first_name.like('%' + args[0] + '%'),
                                                      db.User.last_name.like('%' + args[1].capitalize() + '%')).order_by(
                    db.User.first_name.asc(), db.User.last_name.asc()).from_self()
                if not users.first():
                    users = session.query(db.User).filter(db.User.first_name.like('%' + args[0].capitalize() + '%'),
                                                          db.User.last_name.like('%' + args[1] + '%')).order_by(
                        db.User.first_name.asc(), db.User.last_name.asc()).from_self()
                    if not users.first():
                        bot.send_message(chat_id=update['message']['chat']['id'],
                                         text=messages.usuario_nao_encontrado(update['message']['chat']['first_name']),
                                         parse_mode=ParseMode.HTML)
                        return
    inicio = 0
    if not args:
        pass
    elif args[3] < 0:
        inicio = 0
    elif args[3] > users.count():
        inicio = args[3] - 10
    else:
        inicio = args[3]
    fim = inicio + 10
    for user in users.slice(inicio, fim):
        usuarios += messages.formata_users(user.telegram_id, user.first_name, user.last_name, user.sapu_username)
    session.close()
    mod = divmod(users.count(), 10)
    if mod[1] == 0:
        pag_final = mod[0]
    else:
        pag_final = mod[0] + 1
    usuarios += "\n\nPágina {} de {}".format(int(fim / 10), pag_final)

    keyboard = [[InlineKeyboardButton('Anterior', callback_data='users_anterior {}'.format(inicio)), InlineKeyboardButton('Próxima', callback_data='users_proxima {}'.format(inicio))],
                [InlineKeyboardButton('Sair', callback_data='sair')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if len(args) == 0:
        bot.send_message(chat_id=telegram_id, text=usuarios,
                         reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    elif args[2] == -1:
        bot.send_message(chat_id=telegram_id, text=usuarios,
                         reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        try:
            bot.edit_message_text(chat_id=telegram_id, message_id=args[2],
                                  text=usuarios, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except:
            pass
