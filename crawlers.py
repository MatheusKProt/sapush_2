import lxml.html
import requests
from bs4 import BeautifulSoup

import messages
import util


def get_session(email, password):
    session = requests.session()

    login = session.get('http://sapu.ucpel.edu.br/')
    login_html = lxml.html.fromstring(login.text)

    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

    form['login'] = email
    form['password'] = password

    sapu = session.post('http://sapu.ucpel.edu.br/portal/engine.php?class=LoginForm&method=onLogin', data=form)
    soup = BeautifulSoup(sapu.content, 'html.parser')
    home = session.get("http://sapu.ucpel.edu.br/portal/index.php?class=Dashboard&message=1")
    home_soup = BeautifulSoup(home.content, 'html.parser')

    for index in soup.find_all('script'):
        if str(index.get_text().lstrip()).split("'")[1] == "Erro":
            if "Usuário" in str(index.get_text().lstrip()).split("'")[3]:
                return session, False, "usuario", "", ""
            elif "Senha" in str(index.get_text().lstrip()).split("'")[3]:
                return session, False, "senha", "", ""
            else:
                return session, False, str(index.get_text().lstrip()).split("'")[3], "", ""
        else:
            chave = str(home_soup.find(class_='div_matricula').get_text().lstrip()).split(" ")[1]
            curso = util.formata_curso(str(home_soup.find(class_='div_curso').get_text().lstrip()).split(": ")[1])
            return session, True, "True", chave, curso


def get_notas(user):
    session, _, _, _, _ = get_session(user.sapu_username, user.sapu_password)
    notas = session.get("http://sapu.ucpel.edu.br/portal/engine.php?class=AvaliacaoFormList")
    soup = BeautifulSoup(notas.content, 'html.parser')
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
            detalhe.append(materia)
            detalhe.pop(0)
            notas_detalhe.append(detalhe)
            detalhe = []
            count = 0

    return notas_resumo, notas_detalhe


def get_frequencia(user):
    session, _, _, _, _ = get_session(user.sapu_username, user.sapu_password)
    frequencia = session.get("http://sapu.ucpel.edu.br/portal/engine.php?class=FrequenciaFormList")
    soup = BeautifulSoup(frequencia.content, 'html.parser')

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


def get_horarios(user):
    session, _, _, _, _ = get_session(user.sapu_username, user.sapu_password)
    horarios = session.get("http://sapu.ucpel.edu.br/portal/engine.php?class=HorarioFormList")
    soup = BeautifulSoup(horarios.content, 'html.parser')
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
    return msg


def get_curriculo(user):
    session, _, _, _, _ = get_session(user.sapu_username, user.sapu_password)
    curriculo = session.get("http://sapu.ucpel.edu.br/portal/engine.php?class=MatrizCurricularFormList")
    soup = BeautifulSoup(curriculo.content, 'html.parser')
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
    return msg


def get_historico(user):
    session, _, _, _, _ = get_session(user.sapu_username, user.sapu_password)
    historico = session.get("http://sapu.ucpel.edu.br/portal/engine.php?class=HistoricoFormList&method=imprimir")
    soup = BeautifulSoup(historico.content, 'html.parser')
    index = soup.find('script')
    return str(index.get_text().lstrip()).split("'")[1]


def get_boleto(user):
    session, _, _, _, _ = get_session(user.sapu_username, user.sapu_password)
    boleto = session.get("http://sapu.ucpel.edu.br/portal/engine.php?class=SolicitacaoBoletoFormList&method=emitirBoleto")
    soup = BeautifulSoup(boleto.content, 'html.parser')
    index = soup.find('script')
    return str(index.get_text().lstrip()).split("'")[1]
