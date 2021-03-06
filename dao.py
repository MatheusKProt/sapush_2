import time

from sqlalchemy.orm import sessionmaker

import db
import util

Session = sessionmaker(bind=db.gen_engine(db.get_database_url()))


def set_notas(user, notas_resumo, notas_detalhe, bot):
    if int(time.strftime("%m", time.localtime())) >= 7:
        semestre = str(time.strftime("%Y/2", time.localtime()))
    else:
        semestre = str(time.strftime("%Y/1", time.localtime()))
    for resumo in notas_resumo:
        session = Session()
        notas_resumo_db = session.query(db.NotasResumo).filter_by(user_id=user.telegram_id, materia=str(resumo[0]), semestre=semestre).first()

        user_id = user.telegram_id
        materia = str(resumo[0])
        primeira_av = float(util.verifica_vazio(resumo[1]))
        segunda_av = float(util.verifica_vazio(resumo[2]))
        media = float(util.verifica_vazio(resumo[3]))
        av_complementar = float(util.verifica_vazio(resumo[4]))
        media_final = float(util.verifica_vazio(resumo[5]))

        if not notas_resumo_db:
            notas_resumo_db = db.NotasResumo(user_id, materia, primeira_av, segunda_av, media, av_complementar, media_final, semestre)

            session.add(notas_resumo_db)
            session.commit()
            session.close()
        else:
            notas_resumo_db.user_id = user_id
            notas_resumo_db.materia = materia
            notas_resumo_db.primeira_av = primeira_av
            notas_resumo_db.segunda_av = segunda_av
            notas_resumo_db.media = media
            notas_resumo_db.av_complementar = av_complementar
            notas_resumo_db.media_final = media_final
            notas_resumo_db.semestre = semestre

            session.commit()
            session.close()

    for detalhe in notas_detalhe:
        session = Session()
        resumo = session.query(db.NotasResumo).filter_by(user_id=user.telegram_id, materia=str(detalhe[8]), semestre=semestre).first()
        try:
            notas = session.query(db.NotasDetalhe).filter_by(materia=resumo.id, descricao=detalhe[0], data=detalhe[1], semestre=semestre).first()
        except:
            admins = session.query(db.Admins).all()
            for admin in admins:
                bot.send_message(chat_id=admin.user_id, text=user.telegram_id)
            break

        descricao = detalhe[0]
        materia = resumo.id
        data = detalhe[1]
        peso = float(util.verifica_vazio_menos_um(detalhe[2]))
        nota = float(util.verifica_vazio_menos_um(detalhe[3]))
        peso_x_nota = float(util.verifica_vazio_menos_um(detalhe[5]))
        if not notas:
            notas = db.NotasDetalhe(materia, descricao, data, peso, nota, peso_x_nota, semestre)

            session.add(notas)
            session.commit()
            session.close()
        else:
            notas.materia = materia
            notas.descricao = descricao
            notas.data = data
            notas.peso = peso
            notas.nota = nota
            notas.peso_x_nota = peso_x_nota
            notas.semestre = semestre

            session.commit()
            session.close()
    return


def set_frequencia(user, frequencias):
    if int(time.strftime("%m", time.localtime())) >= 7:
        semestre = str(time.strftime("%Y/2", time.localtime()))
    else:
        semestre = str(time.strftime("%Y/1", time.localtime()))
    for freq in frequencias:
        session = Session()
        frequencia_db = session.query(db.Frequencia).filter_by(user_id=user.telegram_id, materia=str(freq[0]), semestre=semestre).first()

        user_id = user.telegram_id
        materia = str(freq[0])
        frequencia = float(freq[2].split("%")[0])
        faltas = int(freq[3])

        if not frequencia_db:
            frequencia_db = db.Frequencia(user_id, materia, frequencia, faltas, semestre)

            session.add(frequencia_db)
            session.commit()
            session.close()
        else:
            frequencia_db.user_id = user_id
            frequencia_db.materia = materia
            frequencia_db.frequencia = frequencia
            frequencia_db.faltas = faltas
            frequencia_db.semestre = semestre

            session.commit()
            session.close()
    return


def set_push_notas(users, initial, final):
    session = Session()
    push_notas = db.PushNotas(users, initial, final)

    session.add(push_notas)
    session.commit()
    session.close()


def set_push_frequencia(users, initial, final):
    session = Session()
    push_frequencia = db.PushFrequencia(users, initial, final)

    session.add(push_frequencia)
    session.commit()
    session.close()


def set_error(erro):
    session = Session()
    error = db.Error(erro, str(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())))

    session.add(error)
    session.commit()
    session.close()
