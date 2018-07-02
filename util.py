import messages


def verifica_vazio(v):
    if v:
        return v
    else:
        return 0.0


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


def formata_nome_materia(nome):
    materia = ""
    materias = str(nome).split(" ")
    materias.pop(0)
    materias.pop(0)
    for o in materias:
        if o == "I" or o == "II" or o == "III":
            materia += o + " "
        elif o == "A" or o == "DE" or o == "E":
            materia += o.lower() + " "
        else:
            materia += o.capitalize() + " "
    return materia
