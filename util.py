import messages


def verifica_vazio(v):
    if v:
        return v
    else:
        return 0.0


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

    return messages.formata_notas_resumo(formata_nome_materia(notas_resumo.materia), notas_resumo.primeira_av, notas_resumo.segunda_av,
                                         notas_resumo.av_complementar, notas_resumo.media_final, condicao)


def formata_frequencia(frequencia):
    if frequencia.faltas == 1:
        return messages.formata_frequencia(formata_nome_materia_frequencia(frequencia.materia), frequencia.frequencia, frequencia.faltas, "falta")
    else:
        return messages.formata_frequencia(formata_nome_materia_frequencia(frequencia.materia), frequencia.frequencia, frequencia.faltas, "faltas")


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
            or o == "IX" or o == "X" or o == "ACG" or o == "AC" or o == "TCC":
        return o + " "
    elif o == "A" or o == "DE" or o == "E" or o == "DA" or o == "À":
        return o.lower() + " "
    elif "ACG-" in o:
        return "ACG " + o.split("-")[1].capitalize() + " "
    elif "-A" in o or "-B" in o or "-C" in o or "-D" in o or "-E" in o:
        return o + " "
    else:
        return o.capitalize() + " "


def formata_curso(nome):
    curso = ""
    cursos = str(nome).split(" ")
    for o in cursos:
        curso += formata(o)
    return curso
