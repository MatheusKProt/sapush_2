import lxml.html
import requests
from bs4 import BeautifulSoup

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
