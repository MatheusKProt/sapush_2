from functools import wraps

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode, ChatAction

import db
import messages

url = db.get_database_url()
engine = db.gen_engine(url)
Session = sessionmaker(bind=engine)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
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


@restricted
def alert(bot, update, args):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)    # Comando para o bot ficar digitando...
    msg = ""
    count = 0
    for i in args:                                                                           # Varre o args
        if count != 0:                                                                       # Verifica se count é diferente de 0 para separa o id do usuário da msg a ser enviada
            i = str(i).replace("\\n", '\n')                                                  # Adiciona quebra de linha
            msg += i + " "                                                                   # Adiciona espaço entre as palavras
        count += 1
    bot.send_message(chat_id=args[0], text=messages.alert(msg), parse_mode=ParseMode.HTML)   # Envia a msg


@restricted
def statement(bot, update, args):
    bot.sendChatAction(chat_id=update['message']['chat']['id'], action=ChatAction.TYPING)    # Comando para o bot ficar digitando...
    msg = ""
    for i in args:                                                                           # Varre o args
        i = str(i).replace("\\n", '\n')                                                      # Adiciona quebra de linha
        msg += i + " "                                                                       # Adiciona espaço entre as palavras
    session = Session()                                                                      # Conecta com o banco de dados
    users = session.query(db.User)                                                           # Obtem a lista de usuários cadastrados
    for u in users:                                                                          # Varre os usuários
        bot.send_message(chat_id=u[0], text=messages.alert(msg), parse_mode=ParseMode.HTML)  # Envia a msg
    session.close()                                                                          # Fecha a conexão com o banco de dados
