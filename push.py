import logging
import time

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode
from telegram.ext import run_async

import crawlers
import dao
import db
import main
import messages
import util

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

url = db.get_database_url()
engine = db.gen_engine(url)
Session = sessionmaker(bind=engine)


def notas(bot, update):
    session = Session()
    users_count = 0
    initial = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    for user in session.query(db.User):
        if user.push_notas and user.sapu_username != " ":
            users_count += 1
            get_notas(bot, update, user)
    dao.set_push_notas(users_count, initial, time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    session.close()


def frequencia(bot, update):
    session = Session()
    users_count = 0
    initial = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    for user in session.query(db.User):
        if user.push_frequencia and user.sapu_username != " ":
            users_count += 1
            get_frequencia(bot, update, user)
    dao.set_push_frequencia(users_count, initial, time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    session.close()


@run_async
def get_notas(bot, update, user):
    session = Session()
    notas_resumo, notas_detalhe = crawlers.get_notas(user)
    for detalhe in notas_detalhe:
        resumo = session.query(db.NotasResumo).filter_by(user_id=user.telegram_id, materia=detalhe[8]).first()
        detalhe_sapu = session.query(db.NotasDetalhe).filter_by(materia=resumo.id,
                                                                descricao=str(detalhe[0]),
                                                                data=str(detalhe[1]),
                                                                peso=float(util.verifica_vazio_menos_um(detalhe[2])),
                                                                nota=float(util.verifica_vazio_menos_um(detalhe[3])),
                                                                peso_x_nota=float(util.verifica_vazio_menos_um(detalhe[5]))).first()
        if not detalhe_sapu:
            try:
                bot.send_message(chat_id=user.telegram_id,
                                 text=messages.push_grades(user.first_name, util.formata_nome_materia(resumo.materia),
                                                           float(util.verifica_vazio(detalhe[3])),
                                                           resumo.media,
                                                           util.formata_notas_msg(detalhe[3])),
                                 parse_mode=ParseMode.HTML)
            except Exception as error:
                main.error_callback(bot, update, error)
    dao.set_notas(user, notas_resumo, notas_detalhe)
    session.close()


@run_async
def get_frequencia(bot, update, user):
    session = Session()
    frequencias = crawlers.get_frequencia(user)
    for freq in frequencias:
        frequencia_db = session.query(db.Frequencia).filter_by(user_id=user.telegram_id, materia=str(freq[0]),
                                                               frequencia=float(freq[2].split("%")[0]), faltas=int(freq[3])).first()
        if not frequencia_db and float(freq[2].split("%")[0]) != 100:
            try:
                bot.send_message(chat_id=user.telegram_id,
                                 text=messages.push_frequencia(user.first_name, float(freq[2].split("%")[0]),
                                                               util.formata_nome_materia_frequencia(freq[0])[:-1]),
                                 parse_mode=ParseMode.HTML)
            except Exception as error:
                main.error_callback(bot, update, error)
    dao.set_frequencia(user, frequencias)
    session.close()
