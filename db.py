from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


def get_database_url():
    return "postgresql://pi:tqbtj92651@localhost:5432/sapush"


class User(base):
    __tablename__ = 'user'

    telegram_id = Column('telegram_id', Integer, primary_key=True)
    username = Column('username', String)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    sapu_username = Column('sapu_username', String)
    sapu_password = Column('sapu_password', String)
    termos = Column('termos', Boolean)
    push_notas = Column('push_notas', Boolean)
    push_frequencia = Column('push_frequencia', Boolean)
    data_criacao = Column('data_criacao', String)
    chave = Column('chave', String)
    curso = Column('curso', String)

    notas_resumo = relationship("NotasResumo", cascade="all,delete", backref="user")
    frequencia = relationship("Frequencia", cascade="all,delete", backref="user")
    admins = relationship("Admins", cascade="all,delete", backref="user")
    sugestoes = relationship("Sugestoes", cascade="all,delete", backref="user")
    alert = relationship("Alert", cascade="all,delete", backref="user")

    def __init__(self, telegram_id, username, first_name, last_name, sapu_username, sapu_password, termos, push_notas, push_frequencia, data_criacao, chave, curso):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.sapu_username = sapu_username
        self.sapu_password = sapu_password
        self.termos = termos
        self.push_notas = push_notas
        self.push_frequencia = push_frequencia
        self.data_criacao = data_criacao
        self.chave = chave
        self.curso = curso


class Admins(base):
    __tablename__ = 'admins'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.telegram_id'))

    alert = relationship("Alert", cascade="all,delete", backref="admins")
    statement = relationship("Statement", cascade="all,delete", backref="admins")


class NotasResumo(base):
    __tablename__ = 'notas_resumo'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.telegram_id'))
    materia = Column('materia', String)
    primeira_av = Column('primeira_av', Float)
    segunda_av = Column('segunda_av', Float)
    media = Column('media', Float)
    av_complementar = Column('av_complementar', Float)
    media_final = Column('media_final', Float)

    notas_detalhe = relationship("NotasDetalhe", cascade="all,delete", backref="notas_resumo")

    def __init__(self, user_id, materia, primeira_av, segunda_av, media, av_complementar, media_final):
        self.user_id = user_id
        self.materia = materia
        self.primeira_av = primeira_av
        self.segunda_av = segunda_av
        self.media = media
        self.av_complementar = av_complementar
        self.media_final = media_final


class NotasDetalhe(base):
    __tablename__ = 'notas_detalhe'

    id = Column('id', Integer, primary_key=True)
    materia = Column('materia', Integer, ForeignKey('notas_resumo.id'))
    descricao = Column('descricao', String)
    data = Column('data', String)
    peso = Column('peso', Float)
    nota = Column('nota', Float)
    peso_x_nota = Column('peso_x_nota', Float)

    def __init__(self, materia, descricao, data, peso, nota, peso_x_nota):
        self.materia = materia
        self.descricao = descricao
        self.data = data
        self.peso = peso
        self.nota = nota
        self.peso_x_nota = peso_x_nota


class PushNotas(base):
    __tablename__ = 'push_notas'

    id = Column('id', Integer, primary_key=True)
    users = Column('users', Integer)
    initial = Column('initial', String)
    final = Column('final', String)

    def __init__(self, users, initial, final):
        self.users = users
        self.initial = initial
        self.final = final


class PushFrequencia(base):
    __tablename__ = 'push_frequencia'

    id = Column('id', Integer, primary_key=True)
    users = Column('users', Integer)
    initial = Column('initial', String)
    final = Column('final', String)

    def __init__(self, users, initial, final):
        self.users = users
        self.initial = initial
        self.final = final


class Frequencia(base):
    __tablename__ = 'frequencia'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.telegram_id'))
    materia = Column('materia', String)
    frequencia = Column('frequencia', Float)
    faltas = Column('faltas', Integer)

    def __init__(self, user_id, materia, frequencia, faltas):
        self.user_id = user_id
        self.materia = materia
        self.frequencia = frequencia
        self.faltas = faltas


class Sugestoes(base):
    __tablename__ = 'sugestoes'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.telegram_id'))
    sugestao = Column('sugestao', String)
    data = Column('data', String)

    def __init__(self, user_id, sugestao, data):
        self.user_id = user_id
        self.sugestao = sugestao
        self.data = data


class Alert(base):
    __tablename__ = 'alert'

    id = Column('id', Integer, primary_key=True)
    admin = Column('admin', Integer, ForeignKey('admins.id'))
    user_id = Column('user_id', Integer, ForeignKey('user.telegram_id'))
    msg = Column('msg', String)

    def __init__(self, admin, user_id, msg):
        self.admin = admin
        self.user_id = user_id
        self.msg = msg


class Statement(base):
    __tablename__ = 'statement'

    id = Column('id', Integer, primary_key=True)
    admin = Column('admin', Integer, ForeignKey('admins.id'))
    msg = Column('msg', String)

    def __init__(self, admin, msg):
        self.admin = admin
        self.msg = msg


def gen_engine(url):
    engine = create_engine(url)

    base.metadata.create_all(bind=engine)

    return engine
