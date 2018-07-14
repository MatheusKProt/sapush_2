from bs4 import BeautifulSoup

import messages


def verifica_vazio(v):
    if v:
        return v
    else:
        return 0.0


def verifica_vazio_menos_um(v):
    if v:
        return v
    else:
        return -1


def formata_notas_msg(nota):
    if float(verifica_vazio(nota)) < 3:
        return "Não desanime, na próxima você consegue!"
    elif float(verifica_vazio(nota)) >= 7:
        return "Parabéns!"
    else:
        return "Força, você consegue!"


def formata_notas_resumo(notas_resumo):
    if float(notas_resumo.media_final) < 4:
        condicao = "reprovado"
    elif float(notas_resumo.media_final) >= 7:
        condicao = "aprovado"
    else:
        if notas_resumo.av_complementar == "":
            condicao = "em exame"
        else:
            if float(notas_resumo.av_complementar) >= 6:
                condicao = "aprovado"
            else:
                condicao = "reprovado"

    return messages.formata_notas_resumo(formata_nome_materia(notas_resumo.materia), notas_resumo.primeira_av,
                                         notas_resumo.segunda_av,
                                         notas_resumo.av_complementar, notas_resumo.media_final, condicao)


def formata_frequencia(frequencia):
    if frequencia.faltas == 1:
        return messages.formata_frequencia(formata_nome_materia_frequencia(frequencia.materia), frequencia.frequencia,
                                           frequencia.faltas, "falta")
    else:
        return messages.formata_frequencia(formata_nome_materia_frequencia(frequencia.materia), frequencia.frequencia,
                                           frequencia.faltas, "faltas")


def formata_nome_materia(nome):
    materia = ""
    materias = str(nome).split(" ")
    materias.pop(0)
    materias.pop(0)
    for o in materias:
        materia += formata(o)
    return materia


def formata_nome_materia_frequencia(nome):
    materia = ""
    materias = str(nome).split(" ")
    materias.pop(0)
    materias.pop(0)
    materias.pop(0)
    materias.pop(0)
    for o in materias:
        materia += formata(o)
    return materia


def formata(o):
    if o == "I" or o == "II" or o == "III" or o == "IV" or o == "V" or o == "VI" or o == "VII" or o == "VIII" \
            or o == "IX" or o == "X" or o == "ACG" or o == "AC" or o == "TCC" or o == "VLSI" or "-A" in o \
            or "-B" in o or "-C" in o or "-D" in o or "-E" in o or "- A" in o or "- B" in o or "- C" in o or "- D" in o \
            or "- E" in o:
        return o + " "
    elif o == "A" or o == "DE" or o == "E" or o == "DA" or o == "À" or o == "EM" or o == "PARA":
        return o.lower() + " "
    elif "ACG-" in o:
        return "ACG " + o.split("-")[1].capitalize() + " "
    else:
        return o.capitalize() + " "


def formata_curso(nome):
    curso = ""
    cursos = str(nome).split(" ")
    for o in cursos:
        curso += formata(o)
    return curso


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def formata_horarios(index):
    horario = str(index.get_text().lstrip()).split("\n")
    hora = horario[1].split(" - ")
    try:
        inicio = hora[0].split(":")
        inicial = inicio[0] + ":" + inicio[1]
    except:
        inicial = "(horário não cadastrado)"
    try:
        fim = hora[1].split(":")
        final = fim[0] + ":" + fim[1]
    except:
        final = "(horário não cadastrado)"
    predios = horario[2].split(" ")
    predio = ""
    count = 0
    if predios == [' ']:
        for p in predios:
            if count == 0:
                predio += p.lower() + " "
            else:
                predio += p.capitalize() + " "
            count += 1
        predio = predio[:-1]
    else:
        predio = "(prédio não cadastrado)"
    if horario[3]:
        if " " in horario[3]:
            sala = horario[3].lower()
        else:
            sala = "sala " + horario[3]
    else:
        sala = "(sala não cadastrada)"
    return formata_nome_materia_frequencia(horario[0]), inicial, final, predio, sala


def formata_curriculo(index, session):
    # link = "http://sapu.ucpel.edu.br/portal/" + find_between(str(index), 'href="', '">')
    # link = link.split("?")
    # link = "http://sapu.ucpel.edu.br/portal/engine.php?" + link[1]
    # link = link.split("amp;")
    # novo_link = ""
    # for i in link:
    #     novo_link += i
    # pdf = session.get(novo_link)
    # soup = BeautifulSoup(pdf.content, 'html.parser')
    link = ""

    # for i in soup.find_all('script'):
    #     try:
    #         if "pdf" in str(i.get_text().lstrip()).split("'")[1]:
    #             link = "http://sapu.ucpel.edu.br/portal/" + str(i.get_text().lstrip()).split("'")[1]
    #     except:
    #         pass

    curriculo = str(index.get_text().lstrip()).split("\n")
    materia = ""
    materias = str(curriculo[0]).split(" ")
    materias.pop(0)
    materias.pop(0)
    for o in materias:
        materia += o + " "
    ms = materia.split(" - ")
    materia = ""
    for o in ms:
        materia += o + "-"
    mats = materia[:-1].split(" ")
    materia = ""
    for o in mats:
        materia += formata(o)
    return materia[:-1], curriculo[1], link


def formata_disciplinas(disciplinas):
    disc = []
    discs = []
    for disciplina in disciplinas:
        td = []
        if not disciplina[3] in discs:
            discs.append(disciplina[3])
            td.append(disciplina[3])
            if int(disciplina[3]) == 123:
                td.append("\n<b>Regulares</b>")
            elif int(disciplina[3]) == 200:
                td.append("\n<b>Dependências</b>")
            else:
                td.append("\n<b>Outras</b>")
            disc.append(td)
    msg = "<b>Disciplinas</b>\n"
    for d in disc:
        msg += d[1]
        for disciplina in disciplinas:
            if d[0] == disciplina[3]:
                msg += str(messages.formata_disciplinas(formata_nome_materia(disciplina[1])))
        msg += "\n"
    return msg


def push(pushs):
    msg = ""
    for push in pushs:
        msg += messages.push(push.initial, push.users)
    return msg
