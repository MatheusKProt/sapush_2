import logging

from sqlalchemy.orm import sessionmaker
from telegram import ParseMode

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


def notas(bot, update):
    session = Session()
    for user in session.query(db.User):
        if user.push_notas and user.sapu_username != " ":
            notas_resumo, notas_detalhe = crawlers.get_notas(user)
            for detalhe in notas_detalhe:
                resumo = session.query(db.NotasResumo).filter_by(user_id=user.telegram_id, materia=detalhe[8]).first()
                detalhe_sapu = session.query(db.NotasDetalhe).filter_by(materia=resumo.id,
                                                                        descricao=str(detalhe[0]),
                                                                        data=str(detalhe[1]),
                                                                        peso=float(util.verifica_vazio(detalhe[2])),
                                                                        nota=float(util.verifica_vazio(detalhe[3])),
                                                                        peso_x_nota=float(util.verifica_vazio(detalhe[5]))).first()
                if not detalhe_sapu:
                    bot.send_message(chat_id=user.telegram_id,
                                     text=messages.push_grades(user.first_name, util.formata_nome_materia(resumo.materia),
                                                               float(util.verifica_vazio(detalhe[3])), str(detalhe[0]),
                                                               float(util.verifica_vazio(detalhe[5])),
                                                               float(util.verifica_vazio(detalhe[2]))),
                                     parse_mode=ParseMode.HTML)
            dao.set_notas(user, notas_resumo, notas_detalhe)

    session.close()


