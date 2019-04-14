import time

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode
from telegram.ext import run_async

import db

Session = sessionmaker(bind=db.gen_engine(db.get_database_url()))

msg = '''
Agradecemos pelo seu feedback! Entraremos em contato em qualquer circunstância. Muito obrigado mais uma vez por utilizar o serviço!

Caso deseje entrar em contato, fique a vontade para mandar a mensagem que quiser. Estaremos conferindo cada uma.'''


@run_async
def main(bot, update):
    telegram_id = update['message']['chat']['id']
    texto = str(update['message']['text']).lower()
    session = Session()
    admin = session.query(db.Admins).filter_by(user_id=telegram_id).first()
    if not admin:
        session.add(db.Chat(telegram_id, texto, time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())))
        session.commit()
    session.close()
    bot.send_message(chat_id=telegram_id, text=msg, parse_mode=ParseMode.HTML)


@run_async
def unknown(bot, update):
    telegram_id = update['message']['chat']['id']
    texto = str(update['message']['text']).lower()
    session = Session()
    admin = session.query(db.Admins).filter_by(user_id=telegram_id).first()
    if not admin:
        session.add(db.Chat(telegram_id, texto, time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())))
        session.commit()
    session.close()
    bot.send_message(chat_id=telegram_id, text='Olá! Esse serviço foi descontinuado! Não é possível mais, por meio deste, obter suas informações.', parse_mode=ParseMode.HTML)
