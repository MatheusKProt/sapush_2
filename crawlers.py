import lxml.html
import requests
from bs4 import BeautifulSoup

import messages


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
