import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import admins
import config
import users


def main():
    updater = Updater(config.token())
    dp = updater.dispatcher

    updater.dispatcher.add_handler(CallbackQueryHandler(users.button))

    # funções dos usuários
    dp.add_handler(CommandHandler("start", users.start))
    dp.add_handler(CommandHandler("acordo", users.do_you_agree))
    dp.add_handler(CommandHandler("login", users.login, pass_args=True))
    dp.add_handler(CommandHandler("deletar", users.deletar))
    # dp.add_handler(CommandHandler("sugerir", users.sugerir, pass_args=True))
    # dp.add_handler(CommandHandler("notas", users.notas))
    # dp.add_handler(CommandHandler("frequencia", users.frequencia))
    # dp.add_handler(CommandHandler("horarios", users.horarios))
    # dp.add_handler(CommandHandler("historico", users.historico))
    # dp.add_handler(CommandHandler("curriculo", users.curriculo))
    # dp.add_handler(CommandHandler("boleto", users.boleto))
    dp.add_handler(CommandHandler("comandos", users.comandos))
    # dp.add_handler(CommandHandler("termos", users.termos))

    # funções dos administradores
    # dp.add_handler(CommandHandler("users", admins.users))
    dp.add_handler(CommandHandler("alert", admins.alert, pass_args=True))
    dp.add_handler(CommandHandler("statement", admins.statement, pass_args=True))
    # dp.add_handler(CommandHandler("suggestions", admins.suggestions))
    # dp.add_handler(CommandHandler("statistics", admins.statistics))
    # dp.add_handler(CommandHandler("log", admins.log))
    # dp.add_handler(CommandHandler("reboot", admins.reboot))
    # dp.add_handler(CommandHandler("update", admins.update))
    # dp.add_handler(CommandHandler("commands", admins.commands))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
