import datetime
import logging

from telegram import Bot
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, InlineQueryHandler

import admins
import config
import conversation
import push
import users
import dao


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        dao.set_error("Unauthorized")
    except BadRequest:
        dao.set_error("BadRequest")
    except TimedOut:
        dao.set_error("TimedOut")
    except NetworkError:
        dao.set_error("NetworkError")
    except ChatMigrated:
        dao.set_error("ChatMigrated")
    except TelegramError:
        dao.set_error("TelegramError")


def main():
    updater = Updater(config.token())
    bot = Bot(config.token())
    dp = updater.dispatcher
    job = updater.job_queue

    # conversations
    dp.add_handler(conversation.login())
    dp.add_handler(conversation.sugerir())
    dp.add_handler(conversation.poll())

    dp.add_handler(CallbackQueryHandler(users.button))
    dp.add_handler(MessageHandler(Filters.text, users.callback))
    dp.add_handler(InlineQueryHandler(users.inlinequery))
    dp.add_handler(MessageHandler(Filters.voice, users.voice_to_text))

    # entradas invalidas
    dp.add_handler(MessageHandler(Filters.audio, users.invalid))
    dp.add_handler(MessageHandler(Filters.document, users.invalid))
    dp.add_handler(MessageHandler(Filters.contact, users.invalid))
    dp.add_handler(MessageHandler(Filters.game, users.invalid))
    dp.add_handler(MessageHandler(Filters.group, users.invalid))
    dp.add_handler(MessageHandler(Filters.location, users.invalid))
    dp.add_handler(MessageHandler(Filters.photo, users.invalid))
    dp.add_handler(MessageHandler(Filters.reply, users.invalid))
    dp.add_handler(MessageHandler(Filters.sticker, users.invalid))
    dp.add_handler(MessageHandler(Filters.video, users.invalid))
    dp.add_handler(MessageHandler(Filters.video_note, users.invalid))

    # erros
    dp.add_error_handler(error_callback)

    # funções dos usuários
    dp.add_handler(CommandHandler("start", users.start))
    dp.add_handler(CommandHandler("deletar", users.deletar))
    dp.add_handler(CommandHandler("notas", users.notas))
    dp.add_handler(CommandHandler("frequencia", users.frequencia))
    dp.add_handler(CommandHandler("horarios", users.horarios))
    dp.add_handler(CommandHandler("historico", users.historico))
    dp.add_handler(CommandHandler("disciplinas", users.disciplinas))
    dp.add_handler(CommandHandler("provas", users.provas))
    dp.add_handler(CommandHandler("curriculo", users.curriculo))
    dp.add_handler(CommandHandler("atestado", users.atestado))
    dp.add_handler(CommandHandler("boleto", users.boleto))
    dp.add_handler(CommandHandler("chave", users.chave))
    dp.add_handler(CommandHandler("moodle", users.moodle))
    dp.add_handler(CommandHandler("email", users.emails, pass_args=True))
    dp.add_handler(CommandHandler("comandos", users.comandos))
    dp.add_handler(CommandHandler("ajuda", users.ajuda))
    dp.add_handler(CommandHandler("termos", users.termos))
    dp.add_handler(CommandHandler("desenvolvedores", users.desenvolvedores))
    dp.add_handler(CommandHandler("editais", users.editais, pass_args=True))
    dp.add_handler(CommandHandler("noticias", users.noticias))
    dp.add_handler(CommandHandler("minhabiblioteca", users.minhabiblioteca))
    dp.add_handler(CommandHandler("configurar", users.configurar))
    dp.add_handler(CommandHandler("menu", users.menu, pass_args=True))

    # funções dos administradores
    dp.add_handler(CommandHandler("users", admins.users, pass_args=True))
    dp.add_handler(CommandHandler("message", admins.message, pass_args=True))
    dp.add_handler(CommandHandler("alert", admins.alert, pass_args=True))
    dp.add_handler(CommandHandler("breakdown", admins.breakdown, pass_args=True))
    dp.add_handler(CommandHandler("suggestions", admins.suggestions, pass_args=True))
    dp.add_handler(CommandHandler("history", admins.history, pass_args=True))
    dp.add_handler(CommandHandler("push", admins.push, pass_args=True))
    dp.add_handler(CommandHandler("results", admins.results))
    dp.add_handler(CommandHandler("statistics", admins.statistics, pass_args=True))
    dp.add_handler(CommandHandler("reboot", admins.reboot))
    dp.add_handler(CommandHandler("commands", admins.commands))
    dp.add_handler(CommandHandler("errors", admins.errors, pass_args=True))

    # filtra comandos invalidos
    dp.add_handler(MessageHandler(Filters.command, admins.unknown))

    # inicia notificação push
    if datetime.datetime.now().hour >= 23:
        day = datetime.datetime.now().day + 1
        hour = 0
    else:
        day = datetime.datetime.now().day
        hour = datetime.datetime.now().hour + 1
    
    job.run_repeating(push.notas, 1800, first=datetime.datetime.now().replace(day=day, hour=hour, minute=0, second=0, microsecond=0))
    job.run_repeating(push.frequencia, 7200, first=datetime.datetime.now().replace(day=day, hour=hour, minute=0, second=0, microsecond=0))

    admins.start(bot)
    job.run_repeating(admins.alerta_uso, 60, first=datetime.datetime.now())

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
