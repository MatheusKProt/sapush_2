import json

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from telegram import ParseMode

import db
import messages
import util

Session = sessionmaker(bind=db.gen_engine(db.get_database_url()))


def get_login(user, password):
    session = requests.session()
    try:
        sapu = session.post('https://sapu.ucpel.edu.br/index.php?class=LoginForm&method=onLogin', data={
            "login": user,
            "password": password,
        })
        return BeautifulSoup(sapu.content, 'html.parser')
    except:
        try:
            sapu = session.post('https://sapu.ucpel.edu.br/index.php?class=LoginForm&method=onLogin', data={
                "login": user,
                "password": password,
            })
            return BeautifulSoup(sapu.content, 'html.parser')
        except:
            return []


def get_login_completo(email, password):
    session = requests.session()
    sapu = session.post('https://sapu.ucpel.edu.br/index.php?class=LoginForm&method=onLogin', data={
        "login": email,
        "password": password,
    })

    soup = BeautifulSoup(sapu.content, 'html.parser')
    home = session.get("https://sapu.ucpel.edu.br/index.php?class=Dashboard&message=1")

    for index in soup.find_all('script'):
        if str(index.get_text().lstrip()).split("'")[1] == "Erro":
            return False, "", ""
        else:
            home_soup = BeautifulSoup(home.content, 'html.parser')
            chave = str(home_soup.find(class_='div_matricula').get_text().lstrip()).split(" ")[1]
            curso = util.formata_curso(str(home_soup.find(class_='div_curso').get_text().lstrip()).split(": ")[1])
            return True, chave, curso


def get_session(email, password):
    session = requests.session()
    session.post('https://sapu.ucpel.edu.br/engine.php?class=LoginForm&method=onLogin', data={
        "login": email,
        "password": password,
    })
    session.get("https://sapu.ucpel.edu.br/index.php?class=Dashboard&message=1")
    return session


def get_notas(user, bot):
    try:
        try:
            session = get_session(user.sapu_username, user.sapu_password)
            notas = session.get("https://sapu.ucpel.edu.br/engine.php?class=AvaliacaoFormList")
        except:
            session = get_session(user.sapu_username, user.sapu_password)
            notas = session.get("https://sapu.ucpel.edu.br/engine.php?class=AvaliacaoFormList")

        soup = BeautifulSoup(notas.content, 'html.parser')
        if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
            tdatagrid = soup.find_all(class_='tdatagrid_body')

            count = 0
            notas_resumo = []
            resumo = []
            for index in tdatagrid[0].find_all('td'):
                resumo.append(index.get_text().lstrip())
                count += 1
                if count == 6:
                    notas_resumo.append(resumo)
                    resumo = []
                    count = 0

            count = 0
            materia = ""
            materias = []
            notas_detalhe = []
            detalhe = []
            for index in tdatagrid[1].find_all(class_='tdatagrid_group'):
                materias.append(index.get_text().lstrip())
            for index in tdatagrid[1].find_all('td'):
                if str(index.get_text().lstrip() + "\n") in materias:
                    materia = index.get_text().lstrip()
                else:
                    count += 1
                    detalhe.append(index.get_text().lstrip())
                if count == 9:
                    if "(" not in detalhe[0]:
                        detalhe.append(materia)
                        detalhe.pop(0)
                        notas_detalhe.append(detalhe)
                    detalhe = []
                    count = 0
            return notas_resumo, notas_detalhe
        else:
            return [], []
    except Exception as e:
        session = Session()
        admins = session.query(db.Admins).all()
        for admin in admins:
            bot.send_message(chat_id=admin.user_id, text="<b>Erro</b>\n\n/{} | Erro: {}".format(user.telegram_id, e),
                             parse_mode=ParseMode.HTML)
        session.close()
        return [], []


def get_frequencia(user, bot):
    try:
        try:
            session = get_session(user.sapu_username, user.sapu_password)
            frequencia = session.get("https://sapu.ucpel.edu.br/engine.php?class=FrequenciaFormList")
        except:
            session = get_session(user.sapu_username, user.sapu_password)
            frequencia = session.get("https://sapu.ucpel.edu.br/engine.php?class=FrequenciaFormList")

        soup = BeautifulSoup(frequencia.content, 'html.parser')
        if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
            count = 0
            table = []
            td = []
            for index in soup.find(class_='tdatagrid_body').find_all('td'):
                td.append(index.get_text().lstrip())
                count += 1
                if count == 4:
                    table.append(td)
                    td = []
                    count = 0
            return table
        else:
            return []
    except Exception as e:
        session = Session()
        admins = session.query(db.Admins).all()
        for admin in admins:
            bot.send_message(chat_id=admin.user_id, text="<b>Erro</b>\n\n/{} | Erro: {}".format(user.telegram_id, e),
                             parse_mode=ParseMode.HTML)
        session.close()
        return []


def get_horarios(user):
    session = get_session(user.sapu_username, user.sapu_password)
    horarios = session.get("https://sapu.ucpel.edu.br/engine.php?class=HorarioFormList")
    soup = BeautifulSoup(horarios.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        tdatagrid_body = soup.find(class_='tdatagrid_body')
        dias = []
        msg = "<b>Horários</b>"
        for index in tdatagrid_body.find_all(class_='tdatagrid_group'):
            dias.append([index.get_text().lstrip()[:-1], util.find_between(str(index), 'level="', '">')])
        for dia, i in dias:
            msg += "\n\n<b>{}</b>".format(str(dia).capitalize())
            for index in tdatagrid_body.find_all(childof=i):
                materia, inicio, fim, predio, sala = util.formata_horarios(index)
                msg += messages.formata_horario(materia, inicio, fim, predio, sala)
        if not dias:
            msg = messages.horarios_empty(user.first_name)
    else:
        msg = messages.perfil_errado(user.first_name)
    return msg


def get_disciplinas(user):
    session = get_session(user.sapu_username, user.sapu_password)
    disciplinas = session.get("https://sapu.ucpel.edu.br/engine.php?class=MatriculaFormList")
    soup = BeautifulSoup(disciplinas.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        tdatagrid_body = soup.find(class_='tdatagrid_body')
        table = []
        td = []
        count = 0
        for index in tdatagrid_body.find_all('td'):
            td.append(index.get_text().lstrip())
            count += 1
            if count == 5:
                table.append(td)
                td = []
                count = 0
        msg = util.formata_disciplinas(table)
        if not table:
            msg = messages.disciplinas_empty(user.first_name)
    else:
        msg = messages.perfil_errado(user.first_name)
    return msg


def get_curriculo(user):
    session = get_session(user.sapu_username, user.sapu_password)
    curriculo = session.get("https://sapu.ucpel.edu.br/engine.php?class=MatrizCurricularFormList")
    soup = BeautifulSoup(curriculo.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        tdatagrid_body = soup.find(class_='tdatagrid_body')
        semestres = []
        msg = "<b>Matriz Curricular</b>"
        for index in tdatagrid_body.find_all(class_='tdatagrid_group'):
            semestres.append([index.get_text().lstrip()[:-1], util.find_between(str(index), 'level="', '">')])
        for semestre, i in semestres:
            msg += "\n\n<b>{}</b>".format(str(semestre).capitalize())
            for index in tdatagrid_body.find_all(childof=i):
                materia, ch, link = util.formata_curriculo(index, session)
                msg += messages.formata_curriculo(materia, ch, link)
    else:
        msg = messages.perfil_errado(user.first_name)
    return msg


def get_historico(user):
    session = get_session(user.sapu_username, user.sapu_password)
    historico = session.get("https://sapu.ucpel.edu.br/engine.php?class=HistoricoFormList&method=imprimir")
    soup = BeautifulSoup(historico.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        index = soup.find('script')
        msg = messages.historico(str(index.get_text().lstrip()).split("'")[1])
    else:
        msg = messages.perfil_errado(user.first_name)
    return msg


def get_moodle(user):
    session = get_session(user.sapu_username, user.sapu_password)
    historico = session.get("https://sapu.ucpel.edu.br/engine.php?class=LoginMoodle&method=index")
    soup = BeautifulSoup(historico.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        index = soup.find('script')
        return messages.formata_moodle(str(index.get_text().lstrip()).split("'")[1])
    else:
        msg = messages.perfil_errado(user.first_name)
    return msg


def get_emails(user, args):
    session = get_session(user.sapu_username, user.sapu_password)
    historico = session.get("https://sapu.ucpel.edu.br/engine.php?class=MensagemForm&method=inbox")
    soup = BeautifulSoup(historico.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        table = []
        td = []
        count = 0
        for index in soup.find('table').find_all('td'):
            if index.get_text().lstrip():
                td.append(index.get_text().lstrip())
                count += 1
            if count > 2:
                table.append(td)
                count = 0
                td = []
        msg = util.formata_email(table, args)
    else:
        msg = messages.perfil_errado(user.first_name)
    return msg


def get_boleto(user):
    session = get_session(user.sapu_username, user.sapu_password)
    boleto = session.get("https://sapu.ucpel.edu.br/engine.php?class=EmitirBoletoFormList")
    soup = BeautifulSoup(boleto.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        try:
            index = soup.find(class_='tdatagrid_body').find_all('td')[1].find('a')
            url = util.find_between(str(index), "href=\"", "\">")
            boleto = session.get("https://sapu.ucpel.edu.br/engine.php?class=EmitirBoletoFormList&method=onBoleto&target=1&key={}".format(url.split("key=")[1]))
            soup = BeautifulSoup(boleto.content, 'html.parser')
            index = soup.find_all(language="JavaScript")
            return str(index[2].get_text().lstrip()).split("'")[1], True
        except:
            return "Você não possui boletos em aberto", False
    else:
        msg = messages.perfil_errado(user.first_name)
        return msg, False


def get_editais(quantidade):
    session = requests.session()
    editais = session.get("http://www.ucpel.edu.br/portal/?secao=com_editais")
    soup = BeautifulSoup(editais.content, 'html.parser')
    count = 0
    msg = "<b>Editais</b>\n"
    for index in soup.find(id='table').find_all(class_='line link'):
        count += 1
        msg += messages.editais(index.get_text().lstrip()[:-1], str(index).split("'")[1])
        if count >= quantidade:
            break
    return msg


def get_noticias(first=False):
    session = requests.session()
    editais = session.get("http://www.ucpel.edu.br/portal/?secao=noticias")
    soup = BeautifulSoup(editais.content, 'html.parser')
    if first:
        index = soup.find(class_='not_block')
        url = util.find_between(str(index), "href=\"", "\">").replace("amp;", "")
        titulo = index.find(class_='not_titulo').get_text().lstrip()
        return messages.ultima_noticia(url, titulo)
    else:
        msg = "<b>Notícias\n</b>"
        for index in soup.find_all(class_='not_block'):
            url = util.find_between(str(index), "href=\"", "\">").replace("amp;", "")
            data = index.find(class_='not_data').get_text().lstrip()
            titulo = index.find(class_='not_titulo').get_text().lstrip()
            msg += messages.noticia(data, titulo, url)
        return msg


def get_minhabiblioteca(user):
    session = get_session(user.sapu_username, user.sapu_password)
    editais = session.get("https://sapu.ucpel.edu.br/engine.php?class=BibliotecaService&method=loginUser&static=1")
    soup = BeautifulSoup(editais.content, 'html.parser')
    response = json.loads(str(soup))
    return response['message']


def get_atestado_simples(user):
    session = get_session(user.sapu_username, user.sapu_password)
    boleto = session.get("https://sapu.ucpel.edu.br/engine.php?class=MatriculaFormList&method=imprimirSimples")
    soup = BeautifulSoup(boleto.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        index = soup.find_all('script')
        return str(index[1].get_text().lstrip()).split("'")[1]
    else:
        return "ERRO"


def get_atestado_completo(user):
    session = get_session(user.sapu_username, user.sapu_password)
    boleto = session.get("https://sapu.ucpel.edu.br/engine.php?class=MatriculaFormList&method=imprimirCompleto")
    soup = BeautifulSoup(boleto.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        index = soup.find_all('script')
        return str(index[1].get_text().lstrip()).split("'")[1]
    else:
        return "ERRO"


def get_atestado_apto(user):
    session = get_session(user.sapu_username, user.sapu_password)
    boleto = session.get("https://sapu.ucpel.edu.br/engine.php?class=MatriculaFormList&method=imprimirRematricula")
    soup = BeautifulSoup(boleto.content, 'html.parser')
    if not str(soup.find('script').get_text().lstrip()).split("'")[1] == "Erro":
        index = soup.find_all('script')
        return str(index[1].get_text().lstrip()).split("'")[1]
    else:
        return "ERRO"
