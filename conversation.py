import time

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

import crawlers
import dao
import db
import messages
import users

url = db.get_database_url()
engine = db.gen_engine(url)
Session = sessionmaker(bind=engine)


def login():
    def iniciar(bot, update):
        telegram_id = update['message']['chat']['id']
        bot.send_message(chat_id=telegram_id, text=messages.user_login())
        return 'user'

    def get_user(bot, update, user_data):
        text = update['message']['text']
        user_data['user'] = text
        return test_user(bot, update, user_data)

    def test_user(bot, update, user_data):
        telegram_id = update['message']['chat']['id']
        soup = crawlers.get_login(user_data['user'], "pass")
        for index in soup.find_all('script'):
            if str(index.get_text().lstrip()).split("'")[1] == "Erro":
                if "Usuário" in str(index.get_text().lstrip()).split("'")[3]:
                    bot.send_message(chat_id=telegram_id, text=messages.user_invalido_login())
                    users.usage(telegram_id, "Login_user", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
                    return 'user'
                elif "Senha" in str(index.get_text().lstrip()).split("'")[3]:
                    bot.send_message(chat_id=telegram_id, text=messages.pass_login())
                    return 'senha'

    def get_senha(bot, update, user_data):
        text = update['message']['text']
        user_data['senha'] = text
        return test_senha(bot, update, user_data)

    def test_senha(bot, update, user_data):
        telegram_id = update['message']['chat']['id']
        first_name = update['message']['chat']['first_name']
        _, logado, _, chave, curso = crawlers.get_session(user_data['user'], user_data['senha'], html=True)
        if not logado:
            bot.send_message(chat_id=telegram_id, text=messages.pass_invalido_login())
            users.usage(telegram_id, "Login_pass", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
            return 'senha'
        else:
            logar(bot, update, [telegram_id, user_data['user'], user_data['senha'], chave, curso, first_name])
            user_data.clear()
            return -1

    def logar(bot, update, args):
        session = Session()
        user = session.query(db.User).filter_by(telegram_id=args[0]).first()
        user.sapu_username = args[1]
        user.sapu_password = args[2]
        user.chave = args[3]
        user.curso = args[4]

        session.commit()

        user = session.query(db.User).filter_by(telegram_id=args[0]).first()
        notas_resumo, notas_detalhe = crawlers.get_notas(user, bot)
        frequencia = crawlers.get_frequencia(user, bot)

        dao.set_notas(user, notas_resumo, notas_detalhe, bot)
        dao.set_frequencia(user, frequencia)
        session.close()

        bot.send_message(chat_id=args[0], text=messages.valid_login(args[5]), parse_mode=ParseMode.HTML)
        users.menu(bot, update, [])
        users.usage(args[0], "Login", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
        return

    def cancelar(bot, update, user_data):
        telegram_id = update['message']['chat']['id']
        bot.send_message(chat_id=telegram_id, text=messages.cancelar_login())
        user_data.clear()
        return -1

    return ConversationHandler(
        entry_points=[CommandHandler('login', iniciar)],

        states={
            'user': [MessageHandler(Filters.text, get_user, pass_user_data=True)],
            'senha': [MessageHandler(Filters.text, get_senha, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('cancelar', cancelar, pass_user_data=True)]
    )
