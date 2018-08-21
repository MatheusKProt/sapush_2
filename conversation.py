import time

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

import admins
import crawlers
import dao
import db
import messages
import users

Session = sessionmaker(bind=db.gen_engine(db.get_database_url()))


def login():
    def iniciar(bot, update):
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=telegram_id, text=messages.user_login())
        return 'user'

    def get_user(bot, update, user_data):
        text = update['message']['text']
        user_data['user'] = text
        return test_user(bot, update, user_data)

    def test_user(bot, update, user_data):
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
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
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        first_name = update['message']['chat']['first_name']

        logado, chave, curso = crawlers.get_login_completo(user_data['user'], user_data['senha'])

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
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
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


def sugerir():
    def iniciar(bot, update):
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=telegram_id, text=messages.conversation_sugestao())
        return 'sugestao'

    def get_sugestao(bot, update, user_data):
        text = update['message']['text']
        user_data['sugestao'] = text
        return test_sugestao(bot, update, user_data)

    def test_sugestao(bot, update, user_data):
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        if len(user_data['sugestao']) < 10:
            bot.send_message(chat_id=telegram_id, text=messages.conversation_sugestao_invalida())
            return 'sugestao'
        else:
            session = Session()
            sugestao = db.Sugestoes(telegram_id, user_data['sugestao'], time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
            session.add(sugestao)
            bot.send_message(chat_id=telegram_id, text=messages.sugestao(update['message']['chat']['first_name']), parse_mode=ParseMode.HTML)
            session.commit()
            session.close()
            users.usage(telegram_id, "Sugestão", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
            return -1

    def cancelar(bot, update, user_data):
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=telegram_id, text=messages.conversation_cancelar())
        user_data.clear()
        return -1

    return ConversationHandler(
        entry_points=[CommandHandler('sugerir', iniciar)],

        states={
            'sugestao': [MessageHandler(Filters.text, get_sugestao, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('cancelar', cancelar, pass_user_data=True)]
    )


def poll():
    def formata(user_data):
        titulo = user_data['titulo']
        questao = user_data['questao']
        msg = ""
        tam = len(user_data) - 1
        for i in range(1, tam):
            msg += str(i) + " - " + user_data['{}'.format(i)] + "\n"
        return """
<b>{}</b>
{}

{}""".format(titulo, questao, msg)

    def top(user_data):
        titulo = user_data['titulo']
        questao = user_data['questao']
        return """
<b>{}</b>

{}

Seu voto é totalmente anônimo e sua opinião é muito importante para que possamos melhorar cada vez mais.""".format(titulo, questao)

    @admins.restricted
    def criar_votacao(bot, update):
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=telegram_id, text=messages.poll_titulo(update['message']['chat']['first_name']))
        return 'titulo'

    def get_titulo(bot, update, user_data):
        user_data['titulo'] = update['message']['text']
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=telegram_id, text=messages.poll_pergunta())
        return 'questao'

    def get_questao(bot, update, user_data):
        user_data['questao'] = update['message']['text']
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=telegram_id, text=messages.poll_primeira_pergunta())
        return 'resposta'

    def get_resposta(bot, update, user_data):
        if str(update['message']['text']).lower() != "finalizar":
            index = len(user_data) - 1
            user_data['{}'.format(index)] = update['message']['text']
            telegram_id = update['message']['chat']['id']
            bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
            if index < 2:
                bot.send_message(chat_id=telegram_id, text=messages.poll_segunda_pergunta())
            else:
                bot.send_message(chat_id=telegram_id, text=messages.poll_outra_pergunta())
            return 'resposta'
        else:
            telegram_id = update['message']['chat']['id']
            bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
            bot.send_message(chat_id=telegram_id,
                             text=messages.poll_finalizar(formata(user_data)), parse_mode=ParseMode.HTML)
            return 'enviar'

    def enviar(bot, update, user_data):
        if str(update['message']['text']).lower() in ["sim", "s", "y", "enviar"]:
            session = Session()
            poll_db = db.Poll(user_data['titulo'], user_data['questao'])
            session.add(poll_db)
            session.commit()
            keyboard = []
            tam = len(user_data) - 1
            for i in range(1, tam):
                options_poll_db = db.OptionsPoll(poll_db.id, user_data['{}'.format(i)])
                session.add(options_poll_db)
                session.commit()
                keyboard.append([InlineKeyboardButton('{}'.format(user_data['{}'.format(i)]), callback_data='poll | {} | {}'.format(poll_db.id, options_poll_db.id))])
            options_poll_db = db.OptionsPoll(poll_db.id, 'Não sou capaz de opinar')
            session.add(options_poll_db)
            session.commit()
            keyboard.append([InlineKeyboardButton('Não sou capaz de opinar', callback_data='poll | {} | {}'.format(poll_db.id, options_poll_db.id))])
            reply_markup = InlineKeyboardMarkup(keyboard)
            for user in session.query(db.User):
                bot.send_message(chat_id=user.telegram_id, text=top(user_data), reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            user_data.clear()
            session.close()
            return -1
        else:
            telegram_id = update['message']['chat']['id']
            bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
            bot.send_message(chat_id=telegram_id, text=messages.poll_finalizar_dnv())
            return 'enviar'

    def cancelar(bot, update, user_data):
        telegram_id = update['message']['chat']['id']
        bot.sendChatAction(chat_id=telegram_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=telegram_id, text=messages.poll_cancelar(update['message']['chat']['first_name']))
        user_data.clear()
        return -1

    return ConversationHandler(
        entry_points=[CommandHandler('poll', criar_votacao)],

        states={
            'titulo': [MessageHandler(Filters.text, get_titulo, pass_user_data=True)],
            'questao': [MessageHandler(Filters.text, get_questao, pass_user_data=True)],
            'resposta': [MessageHandler(Filters.text, get_resposta, pass_user_data=True)],
            'enviar': [MessageHandler(Filters.text, enviar, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('cancelar', cancelar, pass_user_data=True)]
    )
