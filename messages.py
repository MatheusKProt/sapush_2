from random import randint


def comandos():
    return """
<b>Lista de comandos</b>

/login - realiza o login no SAPU ou altera o login existente
/deletar - deleta suas informações de login do SAPU 
/sugerir - envia uma sugestão aos desenvolvedores do bot
/configurar - configura o estado das notificações push

/notas - exibe suas notas atuais
/frequencia - exibe sua frequência atual
/horarios - exibe seus horários atuais
/disciplinas - exibe suas disciplinas atuais
/provas - exibe as datas de todas as suas provas
/historico - exibe seu histórico 
/curriculo - exibe o currículo do seu curso
/atestado - exibe seu atestado de matrícula
/boleto - exibe o link para acesso
/editais - exibe os últimos editais publicados
/noticias - exibe as últimas notícias acadêmicas 
/chave - exibe sua chave de matrícula
/email - exibe seus últimos emails recebidos
/moodle - exibe o link para acesso
/minhabiblioteca - exibe o link para acesso

/desenvolvedores - exibe os desenvolvedores do bot
/termos - exibe os termos de uso
/ajuda - exibe instruções de uso
/menu - exibe o menu de comandos"""


def comandos_admin():
    return """
<b>Lista de comandos administrativos</b>

/users [nome]* [sobrenome]* - exibe todos os usuários cadastrados
/poll - cria uma enquete e envia a todos os usuários
/results - exibe os resultados da última enquete
/alert [mensagem] - envia um alerta a todos os usuários
/message [id]** [mensagem] - envia uma mensagem para uma pessoa específica
/suggestions [número de sugestões]* ** - exibe as as sugestões recebidas
/history [id/all]* ** [número de resultados]* ** - exibe o histórico de uso das funções de todos os usuários ou de um usuário específico
/push [notas/frequencia]* [número de atualizações]* ** - exibe o status de atualização das notificações push
/errors [número de erros]* ** - exibe erros encontrados durante a execução

/statistics - exibe as estatísticas atuais de uso de hardware
/reboot - reinicia o servidor

*Opcional
**Somente números são aceitos"""


def start(first_name):
    return """
Olá {}!

Se você chegou até aqui, é por que você já sabe qual é a minha utilidade. Mas caso você não saiba, minha utilidade \
é fornecer a você uma forma de fonte única e simples de acompanhar todas as informações armazenadas no SAPU, como avaliações, \
frequência, horários e muito mais, utilizando comandos, mensagens de áudio ou simples perguntas do tipo "Qual é a minha \
chave de matricula?".

Vamos começar? 

Leia com atenção os termos de uso e siga as instruções a seguir para ver tudo o que eu sou capaz de fazer.

<b>Termos de Uso</b>
Pelo acesso e uso deste bot, você aceita e concorda em cumprir os termos legais de uso. Ao utilizar este bot, \
você declara que leu e compreendeu estes termos e condições e concorda em ficar vinculado aos mesmos. \
A utilização dos serviços deste bot requer obrigatória e cumulativamente (i) a realização de cadastro prévio e (ii) \
leitura e aceitação dos termos de uso.

Nós desenvolvedores, juntamente com o serviço prestado, não compactuamos, incentivamos ou promovemos o uso ilegal dos \
seus dados. Nosso objetivo por meio deste é facilitar a sua vida automatizando tarefas do dia a dia. \
Não assumimos qualquer responsabilidade por aqueles que utilizam estes aplicativos para qualquer outra finalidade que \
não o monitoramento próprio do Sistema de Apoio Universitário (SAPU) da Universidade Católica de Pelotas (UCPel).

Caso você queira ler os termos de uso detalhados, utilize o comando /termos.""".format(first_name)


def termos():
    return """
<b>Termos de Uso</b>    
    
<b>Geral</b>
Todas as funcionalidades deste bot estão sujeitos aos termos e condições dos contratos aplicáveis que \
regem seu uso, que podem mudar de tempos em tempos. No caso de qualquer conflito, os termos fornecidos aqui \
prevalecerão. Os recursos e conteúdos fornecidos por este podem ser alterados a qualquer momento sem aviso prévio. \
Acredita-se que as informações fornecidas por este sejam confiáveis quando postadas, mas não há garantia de que elas \
sejam precisas, completas ou atuais em todos os momentos. Devido à natureza dinâmica da internet, os \
recursos que estão disponíveis no bot podem ser removidos a qualquer momento, e a localização dos itens pode mudar à \
medida que menus e funcionalidades são reorganizados. O usuário concorda expressamente que o uso deste bot é de sua total \
responsabilidade. Nenhum material pode ser modificado, editado ou retirado de contexto, de modo que seu uso crie uma \
declaração ou impressão falsa ou enganosa sobre as posições, declarações, informações ou ações.

<b>Condições para Produtos e Serviços</b>
Os termos e condições aplicáveis a qualquer produto, serviço ou informação serão aqueles determinados no momento \
da prestação do produto, serviço ou informação. Se você optar por acessar este bot, você o faz por iniciativa própria \
e é responsável pela conformidade com as leis locais, nacionais ou internacionais aplicáveis.

<b>Confidencialidade</b>
Trataremos todas as informações a seu respeito como confidenciais. Não divulgaremos qualquer informação \
que detenhamos sobre você, exceto nas seguintes circunstâncias: (i) sob obrigação de fazê-lo sob a lei brasileira e \
(ii) onde você forneceu sua autorização prévia por escrito para fazê-lo. Você não pode usar, exportar ou reexportar as \
informações ou qualquer cópia ou adaptação em violação de quaisquer leis ou regulamentos aplicáveis."

<b>Garantia</b>
Nós, desenvolvedores do bot, não fazemos quaisquer garantias, declarações, endossos ou condições, expressas ou implícitas, \
com relação ao bot ou as informações contidas nele, incluindo, sem limitação, garantias de comerciabilidade, operação, \
não infração, utilidade, integridade, precisão, atualidade, confiabilidade e adequação a uma finalidade específica. \
Além disso, não representamos ou garantimos que o bot estará disponível e atenderá aos seus requisitos, que o acesso \
será ininterrupto, que não haverá atrasos, falhas, erros, omissões ou perda de informações transmitidas, que nenhum \
vírus ou outra contaminação ou propriedades destrutivas serão transmitidas ou que nenhum dano ocorrerá no sistema do \
seu computador e/ou celular. Você é o único responsável pela proteção e backup adequados de dados e/ou equipamentos \
e por tomar precauções razoáveis e apropriadas para verificar se há vírus de computador ou outras propriedades destrutivas.

<b>Copyright Universidade Católica de Pelotas (UCPel)</b>
Todos os textos, imagens, gráficos, animações, vídeos, músicas, sons e outros materiais \
são protegidos por direitos autorais e outros direitos de propriedade intelectual pertencentes à Universidade Católica \
de Pelotas, suas subsidiárias, afiliadas e licenciantes.

Este projeto <b>não</b> é oficialmente afiliado com a instituição de ensino Universidade Católica de Pelotas (UCPel).

Por favor, ajude-nos a melhorar. Caso haja alguma dúvida ou sugestão, entre em contato utilizando o comando \
/desenvolvedores."""


def not_logged_in(first_name):
    return """
{}, para ter acesso a esta funcionalidade você deverá realizar o login em seu SAPU utilizando o comando \
/login.

O usuário e a senha devem ser os mesmos utilizados no SAPU.""".format(first_name)


def login_invalid(first_name):
    return """
{}, você alterou sua senha ou seu e-mail do SAPU recentemente? Achamos que sim. Se você quiser continuar recebendo \
todas as informações que o bot pode fornecer, por favor, faça a autenticação novamente utilizando o comando /login.""".format(first_name)


def message(msg, admin, user):
    return """
<b>Mensagem</b>
De <b>{}</b> para <b>{}</b>:

{}""".format(admin, user, msg)


def alert(msg):
    return """
<b>Comunicado</b>

{}""".format(msg)


def invalid_login(first_name):
    return """
{}, utilize o comando /login.

O usuário e a senha devem ser os mesmos utilizados no SAPU.""".format(first_name)


def valid_login(first_name):
    return """
{}, seu login foi efetuado com sucesso!""".format(first_name)


def suggest_without_parameters(first_name):
    return """
{}, utilize o comando /sugerir.""".format(first_name)


def not_registered(first_name):
    return """
{}, para ter acesso a esta funcionalidade você deverá realizar o login em seu SAPU utilizando o \ 
comando /login.

O usuário e a senha devem ser os mesmos utilizados no SAPU.""".format(first_name)


def push_grades(first_name, materia, nota, media, msg):
    return """
{}, sua nota de <b>{}</b>acabou de ser publicada no sistema!
Você tirou <b>{}</b> de 10.0.
Sua média atual é <b>{}</b>.
<b>{}</b>""".format(first_name, materia, nota, media, msg)


def push_provas(first_name, materia):
    return """
{}, sua avaliação de <b>{}</b> foi alterada. Por favor, verifique através do comando /provas.""".format(first_name, materia[:-1])


def push_grades_null(first_name, materia, data):
    return """
{}, sua avaliação de <b>{}</b> acabou de ser cadastrada no sistema e está marcada para o dia <b>{}</b>.
Bons estudos!""".format(first_name, materia, data)


def push_frequencia(first_name, frequencia, materia):
    return """
{}, você está com <b>{}%</b> de frequência em <b>{}</b>. 
Tome cuidado para não reprovar!""".format(first_name, frequencia, materia)


def not_allowed(first_name):
    return """
{}, esta função não está habilitada para você.""".format(first_name)


def not_agreed(first_name):
    return """
{}, esta função não está habilitada para você. Utilize o comando /start e siga as instruções.""".format(first_name)


def agreed(first_name):
    return """
{}, você já aceitou os termos de uso.""".format(first_name)


def user_doesnt_exist(first_name):
    return """
{}, não há informações de login para deletar.""".format(first_name)


def delete_user(first_name):
    return """
{}, você tem certeza que deseja deletar suas informações? \
Se você fizer isso, você não poderá acessar mais nenhuma funcionalidade que este bot oferece.""".format(first_name)


def user_deleted(first_name):
    return """
{}, suas informações de login foram deletadas com sucesso!""".format(first_name)


def do_you_agree():
    return """
Você leu e concorda com os termos de uso?"""


def yes():
    return """
Você concordou com os termos de uso."""


def login_requirement():
    return """
Para ter acesso a todas as funcionalidades você deverá realizar o login em seu SAPU utilizando o comando /login.

O usuário e a senha devem ser os mesmos utilizados no SAPU.

Caso necessite de auxilio, digite ajuda a qualquer momento."""


def no(first_name):
    return """
{}, suas funcionalidades não estão habilitadas. Você não poderá utilizar o bot enquanto não aceitar os termos de uso. \
Caso você mude de ideia, utilize o comando /start e siga as instruções.""".format(first_name)


def formata_notas_resumo(materia, primeira_av, segunda_av, av_complementar, media_final, condicao):
    return """
<b>{}</b>
<b>{}</b> na primeira avaliação
<b>{}</b> na segunda avaliação
<b>{}</b> de avaliação complementar
<b>{}</b> de média final
Até o momento, você está <b>{}</b>.""".format(materia, primeira_av, segunda_av, av_complementar, media_final, condicao)


def formata_frequencia(materia, frequencia, faltas, falta_msg):
    return """
<b>{}</b>
<b>{}%</b> de frequência
<b>{}</b> {}""".format(materia, frequencia, faltas, falta_msg)


def help_user(first_name):
    return """
<b>Ajuda</b>

{}, você pediu por ajuda. Sendo assim, vou lhe mostrar algumas dicas de como tirar proveito de todas as funcionalidades disponíveis.

Ao utilizar o bot, você provavelmente se deparou com uma nova sintaxe para troca de mensagens: o uso da / antes de uma mensagem. Essa barra significa, na verdade, que a palavra que segue a mensagem é um comando. Qualquer função que vocë precisar acessar, você recorrerá a ela.

/notas é um exemplo de comando disponível.

Caso haja alguma dúvida quanto ao funcionamento, você poderá entrar em contato a qualquer hora através do comando /desenvolvedores, clicando em um dos desenvolvedores. Não se acanhe, faremos o possível para ajudar. 

Recomendamos que você assista ao <a href="https://youtu.be/B38cJfpi4XU">vídeo de demonstração do bot</a> se estiver perdido e não sabe por onde começar. 

Ao ler estas informações, esperamos que você esteja apto a utilizar o bot de maneira satisfatória.

Obs: algumas funções foram alteradas no decorrer do desenvolvimento, com o intuíto de simplificar o uso do bot, e não funcionam mais da mesma forma retratada no vídeo de demonstração.""".format(first_name)


def historico(historico):
    return """
<b>Histórico</b>

Seu histórico está disponível <a href=\"http://sapu.ucpel.edu.br/portal/{}\">aqui</a>.""".format(historico)


def boleto(first_name, boleto, option):
    if option == 1:
        return """
<b>Boleto</b>

Seu boleto está disponível <a href=\"http://sapu.ucpel.edu.br/portal/{}\">aqui</a>.""".format(boleto)
    else:
        return """
{}, você não possui boletos em aberto.""".format(first_name)


def formata_users(telegram_id, first_name, last_name, sapu_username):
    if not last_name:
        last_name = ""
    if sapu_username == " ":
        return """
/{} | {} {}""".format(telegram_id, first_name, last_name)
    else:
        return """
/{} | <b>{} {}</b>""".format(telegram_id, first_name, last_name)


def formata_sugestoes(first_name, last_name, sugestao):
    return """
{} {}: {}""".format(first_name, last_name, sugestao)


def formata_error(erro, data):
    return """
{} | {}""".format(data, erro)


def usuario_nao_encontrado(first_name):
    return """
{}, não encontrei nenhum usuário com esses parâmetros.""".format(first_name)


def sugestao(first_name):
    return """
{}, agradecemos sua sugestão! 
Faremos o possível para implementá-la nas próximas atualizações.""".format(first_name)


def alert_error(first_name):
    return """
{}, utilize o comando /message [id]** [mensagem].

**Somente números são aceitos""".format(first_name)


def statement_error(first_name):
    return """
{}, utilize o comando /alert [mensagem].""".format(first_name)


def alert_success(first_name, user):
    return """
{}, sua mensagem para {} foi enviada com sucesso!""".format(first_name, user)


def statistics(ligado, uso_processador, uso_memoria, uso_disco, memoria_total, memoria_usada, memoria_disponivel, disco_total,
               disco_usado, disco_disponivel, processos_consumindo):
    return """
<b>Estatísticas de uso do servidor</b>
{}
Processador: {}%
Memória: {}%
Disco: {}%

Memória total: {}GB
Memória usada: {}GB
Memória disponível: {}GB

Disco total: {}GB
Disco usado: {}GB
Disco disponível: {}GB

Os processos com maior consumo de memória são:{}""".format(ligado, uso_processador, uso_memoria, uso_disco,
                                                           round(memoria_total, 2), round(memoria_usada, 2),
                                                           round(memoria_disponivel, 2), round(disco_total, 2),
                                                           round(disco_usado, 2), round(disco_disponivel, 2),
                                                           processos_consumindo)


def formata_horario(materia, inicio, fim, predio, sala):
    return """
<b>{}</b>
Das {} até as {} no {}, {}.""".format(materia, inicio, fim, predio, sala)


def formata_curriculo(materia, ch, link):
    return """
<a href=\"{}\">{}</a> | {}""".format(link, ch, materia)


def notas_empty(first_name):
    return """
{}, ainda não há notas cadastradas no SAPU.""".format(first_name)


def frequencia_empty(first_name):
    return """
{}, ainda não há frequência cadastrada no SAPU.""".format(first_name)


def horarios_empty(first_name):
    return """
{}, ainda não há horários cadastrados no SAPU.""".format(first_name)


def disciplinas_empty(first_name):
    return """
{}, ainda não há disciplinas cadastradas no SAPU.""".format(first_name)


def count_users(first_name, num):
    return """
{}, o número total de usuários é {}.""".format(first_name, num)


def not_registered(first_name):
    return """
{}, para ter acesso a esta funcionalidade utilize o comando /start.""".format(first_name)


def formata_disciplinas(disciplina):
    return """
{}""".format(disciplina)


def chave(chave):
    return """
<b>Chave</b>

Sua chave de matrícula é {}.""".format(chave)


def push(initial, final, users):
    return """
{} | {} | {}""".format(initial, final, users)


def developers():
    return """
<b>Desenvolvedores</b>

Este bot foi desenvolvido com muita dedicação por <a href="https://t.me/lucaspeferreira">Lucas Ferreira</a> e \
<a href="https://t.me/matheuskprot">Matheus Protzen</a>.

Caso você queira falar com um de nós, basta clicar no nosso nome e enviar uma mensagem. Faremos o possível para lhe ajudar."""


def editais(nome, link):
    return """
{} | <a href=\"{}\">acesse aqui</a>.""".format(nome, link)


def no_suggestions():
    return """
Ainda não há sugestões cadastradas."""


def no_error():
    return """
Ainda não há erros."""


def configurar():
    return """
Você deseja configurar as notificações de qual funcionalidade?"""


def configurar_notas():
    return """
O que você deseja fazer com as notificações relacionadas as notas?"""


def configurar_frequencia():
    return """
O que você deseja fazer com as notificações relacionadas a frequência?"""


def configurar_notas_ativado(first_name):
    return """
{}, as notificações relacionadas as notas foram ativadas.""".format(first_name)


def configurar_notas_desativado(first_name):
    return """
{}, as notificações relacionadas as notas foram desativadas.""".format(first_name)


def configurar_frequencia_ativado(first_name):
    return """
{}, as notificações relacionadas a frequência foram ativadas.""".format(first_name)


def configurar_frequencia_desativado(first_name):
    return """
{}, as notificações relacionadas a frequência foram desativadas.""".format(first_name)


def not_delete_account(first_name):
    return """
{}, você optou por não deletar suas informações.""".format(first_name)


def atestado():
    return """
Você deseja receber qual atestado de matrícula?"""


def formata_atestado(nome, atestado):
    return """
<b>Atestado de Matrícula</b>

Seu atestado de matrícula {}está disponível <a href=\"http://sapu.ucpel.edu.br/portal/{}\">aqui</a>.""".format(nome, atestado)


def formata_moodle(moodle):
    return """
<b>Moodle</b>

Para acessar o moodle, clique <a href=\"{}\">aqui</a>.""".format(moodle)


def formata_email(de, assunto, data):
    return """
De: {}
Assunto: {}
Data: {}
""".format(de, assunto, data[:-3])


def formata_usage(func, num):
    return """
{} | {}""".format(num, func)


def formata_history(data, func, nome):
    return """
{} | {} | {}""".format(data, func, nome)


def speech_error(first_name):
    return """
{}, não entendi o que você falou.""".format(first_name)


def speech_request_error(first_name):
    return """
{}, não consegui processar o seu audio. Que tal enviar outro?""".format(first_name)


def start_server():
    return """
<b>Comunicado</b>

O servidor foi reiniciado ou atualizado com sucesso."""


def invalid(first_name):
    random = randint(0, 2)
    if random == 0:
        return """{}, estou aprendendo a interpretar contextos e em breve poderei conversar com você de forma natural.""".format(first_name)
    elif random == 1:
        return """{}, não entendi o que você falou.""".format(first_name)
    else:
        return """{}, meus desenvolvedores ainda não me deram inteligência suficiente para lidar com isso.""".format(first_name)


def unknown_command(first_name):
    random = randint(0, 1)
    if random == 0:
        return """
{}, este comando é inválido.""".format(first_name)
    else:
        return """
{}, ainda não conheço esse comando.""".format(first_name)


def formata_provas(data, detalhe):
    return """
{} | {}""".format(data, detalhe)


def bugged(first_name):
    return """
{}, esta funcionalidade está em manutenção no momento.""".format(first_name)


def user_login():
    return """
Por favor, digite seu nome de usuário do SAPU.

O usuário deve ser o mesmo utilizado no SAPU."""


def user_invalido_login():
    return """
Usuario inválido. Por favor, digite novamente.

Fique atento ao uso correto do usuário. Você pode usar tanto o seu CPF quanto seu e-mail cadastrado no SAPU.

Caso você queira cancelar o processo de login, utilize o comando /cancelar."""


def pass_login():
    return """
E agora digite a sua senha.

A senha deve ser a mesma utilizada no SAPU."""


def pass_invalido_login():
    return """
Senha inválida. Por favor, digite novamente.

Fique atento ao uso de letras maiúsculas e minúsculas, visto que o SAPU diferencia tais argumentos.

Caso você queira cancelar o processo de login, utilize o comando /cancelar."""


def cancelar_login():
    return """
O processo de login foi cancelado. Caso você precise de auxílio, peça a qualquer momento através do comando /ajuda ou \
entre em contato através do comando /desenvolvedores."""


def conversation_sugestao():
    return """
Por favor, digite a sua sugestão:

Caso você queira cancelar o envio da sua sugestão, utilize o comando /cancelar."""


def conversation_sugestao_invalida():
    return """
Sugestão inválida. O número mínimo de caracteres é 10.

Caso você queira cancelar envio da sua sugestão, utilize o comando /cancelar."""


def conversation_cancelar():
    return """
Você cancelou o envio da sua sugestão. Por favor, não se acanhe!"""


def noticia(data, titulo, url):
    return """
{} | <a href=\"http://www.ucpel.edu.br/portal/{}\">{}</a>""".format(data, url, titulo)


def ultima_noticia(url, titulo):
    return """
Essa é a última notícia acadêmica que foi publicada no portal da UCPel:

<a href=\"http://www.ucpel.edu.br/portal/{}\">{}</a>""".format(url, titulo)


def poll_titulo(first_name):
    return """
{}, qual é o título da sua enquete?""".format(first_name)


def poll_pergunta():
    return """
Pronto. E agora, o que você quer perguntar?"""


def poll_primeira_pergunta():
    return """
Anotado. Digite a primeira alternativa."""


def poll_segunda_pergunta():
    return """
Anotado. Digite a segunda alternativa."""


def poll_outra_pergunta():
    return """
E agora digite a próxima ou digite finalizar."""


def poll_finalizar(conteudo):
    return """
{}
Pronto para enviar? Caso contrário, utilize o comando /cancelar.""".format(conteudo)


def poll_finalizar_dnv():
    return """
Pronto para enviar? Caso contrário, utilize o comando /cancelar."""


def poll_cancelar(first_name):
    return """
{}, você cancelou o envio da enquete.""".format(first_name)


def poll_agradecimento(first_name):
    return """
{}, agradecemos pela sua opinião!""".format(first_name)


def perfil(user, curso, telegram_id, logado, termos, push_notas, push_frequencia, hist):
    return """<b>Perfil</b>

{}
{}
<a href="tg://user?id={}">Contato</a>

<b>Configurações</b>

Logado: {}
Termos: {}
Notas: {}
Frequência: {}

<b>Histórico</b>

{}""".format(user, curso, telegram_id, logado, termos, push_notas, push_frequencia, hist)


def formata_poll(titulo, pergunta, msg, total):
    return """
<b>{}</b>

{}

{}Total de votos: {}""".format(titulo, pergunta, msg, total)


def minhabiblioteca(url):
    return """
<b>Minha Biblioteca</b>

Para acessar a minha biblioteca, clique <a href=\"{}\">aqui</a>.""".format(url)
