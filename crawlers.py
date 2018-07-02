import lxml.html
import requests
from bs4 import BeautifulSoup

import dao


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
    session.get("http://sapu.ucpel.edu.br/portal/index.php?class=Dashboard&message=1")

    for index in soup.find_all('script'):
        if str(index.get_text().lstrip()).split("'")[1] == "Erro":
            if "Usuário" in str(index.get_text().lstrip()).split("'")[3]:
                return session, False, "usuario"
            elif "Senha" in str(index.get_text().lstrip()).split("'")[3]:
                return session, False, "senha"
            else:
                return session, False, str(index.get_text().lstrip()).split("'")[3]
        else:
            return session, True, "True"


def get_notas(user):
    session, _, _ = get_session(user.sapu_username, user.sapu_password)
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
