from sqlalchemy.orm import sessionmaker

import db
import util

url = db.get_database_url()
engine = db.gen_engine(url)
Session = sessionmaker(bind=engine)


def set_notas(user, notas_resumo, notas_detalhe):
    for resumo in notas_resumo:
        session = Session()
        materias = session.query(db.NotasResumo).filter_by(user_id=user.telegram_id, materia=str(resumo[0])).first()

        user_id = user.telegram_id
        materia = str(resumo[0])
        primeira_av = float(util.verifica_vazio(resumo[1]))
        segunda_av = float(util.verifica_vazio(resumo[2]))
        media = float(util.verifica_vazio(resumo[3]))
        av_complementar = float(util.verifica_vazio(resumo[4]))
        media_final = float(util.verifica_vazio(resumo[5]))
        if not materias:
            materias = db.NotasResumo(user_id, materia, primeira_av, segunda_av, media, av_complementar, media_final)

            session.add(materias)
            session.commit()
            session.close()
        else:
            materias.user_id = user_id
            materias.materia = materia
            materias.primeira_av = primeira_av
            materias.segunda_av = segunda_av
            materias.media = media
            materias.av_complementar = av_complementar
            materias.media_final = media_final

            session.commit()
            session.close()

    for detalhe in notas_detalhe:
        session = Session()
        resumo = session.query(db.NotasResumo).filter_by(user_id=user.telegram_id, materia=str(detalhe[8])).first()
        session.close
        session = Session()
        notas = session.query(db.NotasDetalhe).filter_by(materia=resumo.id, descricao=detalhe[0]).first()

        descricao = detalhe[0]
        materia = resumo.id
        data = detalhe[1]
        peso = float(util.verifica_vazio(detalhe[2]))
        nota = float(util.verifica_vazio(detalhe[3]))
        peso_x_nota = float(util.verifica_vazio(detalhe[5]))
        if not notas:
            notas = db.NotasDetalhe(materia, descricao, data, peso, nota, peso_x_nota)

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

            session.commit()
            session.close()
    return
