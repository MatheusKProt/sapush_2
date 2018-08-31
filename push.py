import logging
import psutil
import threading
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

Session = sessionmaker(bind=db.gen_engine(db.get_database_url()))


@run_async
def notas(bot, update):
    session = Session()
    users_count = 0
    initial = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    for user in session.query(db.User):
        if user.push_notas and user.sapu_username != " ":
            try:
                soup = crawlers.get_login(user.sapu_username, user.sapu_password)
                if str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
                    if "Usuário" in str(soup.find('script').get_text().lstrip()).split("'")[3] or "Senha" in str(soup.find('script').get_text().lstrip()).split("'")[3]:
                        bot.send_message(chat_id=user.telegram_id, text=messages.login_invalid(user.first_name), parse_mode=ParseMode.HTML)
                        dao.set_error("Login inválido /{}".format(user.telegram_id))
                        user_db = session.query(db.User).filter_by(telegram_id=user.telegram_id).first()
                        user_db.sapu_username = " "
                        user_db.sapu_password = " "
                        session.commit()
                else:
                    t = threading.Thread(target=get_notas, args=(bot, update, user))
                    while psutil.cpu_percent(0.3) > 60:
                        time.sleep(0.7)
                    t.start()
                    users_count += 1
            except:
                pass
    dao.set_push_notas(users_count, initial, time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    session.close()


@run_async
def frequencia(bot, update):
    session = Session()
    users_count = 0
    initial = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    for user in session.query(db.User):
        if user.push_frequencia and user.sapu_username != " ":
            try:
                soup = crawlers.get_login(user.sapu_username, user.sapu_password)
                if str(soup.find('script').get_text().lstrip()).split("'")[1] != "Erro":
                    t = threading.Thread(target=get_frequencia, args=(bot, update, user))
                    while psutil.cpu_percent(0.3) > 60:
                        time.sleep(0.7)
                    t.start()
                    users_count += 1
            except:
                pass
    dao.set_push_frequencia(users_count, initial, time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    session.close()


def get_notas(bot, update, user):
    session = Session()
    notas_resumo, notas_detalhe = crawlers.get_notas(user, bot)
    for detalhe in notas_detalhe:
        resumo = session.query(db.NotasResumo).filter_by(user_id=user.telegram_id, materia=detalhe[8]).first()
        if not resumo:
            try:
                bot.send_message(chat_id=user.telegram_id,
                                 text=messages.push_grades_null(user.first_name, str(detalhe[0]).split(" - ")[0].lower(),
                                                                util.formata_nome_materia(detalhe[8])[:-1], detalhe[1]),
                                 parse_mode=ParseMode.HTML)
            except Exception as error:
                main.error_callback(bot, update, error)
        else:
            detalhe_sapu = session.query(db.NotasDetalhe).filter_by(materia=resumo.id, descricao=str(detalhe[0]),
                                                                    data=str(detalhe[1]), peso=float(util.verifica_vazio_menos_um(detalhe[2])),
                                                                    nota=float(util.verifica_vazio_menos_um(detalhe[3])),
                                                                    peso_x_nota=float(util.verifica_vazio_menos_um(detalhe[5]))).first()
            if not detalhe_sapu:
                detalhe_sapu = session.query(db.NotasDetalhe).filter_by(materia=resumo.id, descricao=str(detalhe[0]), data=str(detalhe[1])).first()
                if detalhe_sapu:
                    try:
                        bot.send_message(chat_id=user.telegram_id,
                                         text=messages.push_grades(user.first_name, util.formata_nome_materia(resumo.materia),
                                                                   float(util.verifica_vazio(detalhe[3])), resumo.media,
                                                                   util.formata_notas_msg(detalhe[3])),
                                         parse_mode=ParseMode.HTML)
                    except Exception as error:
                        main.error_callback(bot, update, error)
                else:
                    bot.send_message(chat_id=user.telegram_id,
                                     text=messages.push_provas(user.first_name, util.formata_nome_materia(resumo.materia)),
                                     parse_mode=ParseMode.HTML)
    dao.set_notas(user, notas_resumo, notas_detalhe, bot)
    session.close()


def get_frequencia(bot, update, user):
    session = Session()
    frequencias = crawlers.get_frequencia(user, bot)
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
