from random import randint


def obrigado(first_name):
    random = randint(0, 1)
    if random == 0:
        return """
Merece, {}!""".format(first_name)
    else:
        return """
Ao seu dispor!"""


def oi(first_name):
    return """
Oi, {}! O que você vai consultar hoje?""".format(first_name)


def ola(first_name):
    return """
Olá, {}! O que você vai consultar hoje?""".format(first_name)


def ok():
    return """
👍"""


def risos():
    return """
😂😂😂"""
