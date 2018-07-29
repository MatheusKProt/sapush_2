def comandos():
    return """
<b>Lista de comandos</b>

/login [usuário] [senha] - faz o login no SAPU ou altera o login existente
/deletar - deleta suas informações de login do SAPU 
/sugerir [mensagem] - envia uma sugestão aos desenvolvedores 
/configurar - configura o estado das notificações push

/notas - retorna suas notas do semestre atual 
/frequencia - retorna sua frequência do semestre atual 
/horarios - retorna seus horários do semestre atual 
/disciplinas - retorna suas disciplinas do semestre atual
/historico - retorna seu histórico 
/curriculo - retorna o currículo do curso
/atestado - retorna seu atestado de matrícula
/boleto - retorna o link com seu boleto
/editais - retorna os ultimos editais publicados
/chave - retorna sua chave de matrícula
/email - retorna os últimos emails recebidos
/moodle - retorna o link com o moodle logado

/desenvolvedores - exibe os desenvolvedores do bot
/termos - exibe os termos de uso
/ajuda - exibe instruções de uso
/menu - exibe o menu de comandos*

*Funcionalidade em fase de testes"""


def comandos_admin():
    return """
<b>Lista de comandos administrativos</b>

/users [nome/count]* [sobrenome]* - exibe todos os usuários cadastrados
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
frequência, horários e muito mais. 

Vamos começar? 

Leia com atenção os Termos de Uso e siga as instruções a seguir para ver tudo o que eu sou capaz de fazer.

<b>Termos de Uso</b>
Pelo acesso e uso deste bot, você aceita e concorda em cumprir os termos legais de uso. Ao utilizar este bot, \
você declara que leu e compreendeu estes termos e condições e concorda em ficar vinculado aos mesmos. \
A utilização dos serviços deste bot requer obrigatória e cumulativamente (i) a realização de cadastro prévio e (ii) \
leitura e aceitação dos Termos de Uso.

Nós desenvolvedores, juntamente com o serviço prestado, não compactuamos, incentivamos ou promovemos o uso ilegal dos \
seus dados. Nosso objetivo por meio deste é facilitar a sua vida automatizando tarefas do dia a dia. \
Não assumimos qualquer responsabilidade por aqueles que utilizam estes aplicativos para qualquer outra finalidade que \
não o monitoramento próprio do Sistema de Apoio Universitário (SAPU) da Universidade Católica de Pelotas.

Caso você queira ler os Termos de Uso detalhados, utilize o comando /termos.""".format(first_name)


def termos():
    return """
<b>Termos de Uso</b>    
    
<b>Geral</b>
Todas as funcionalidades deste bot estão sujeitos aos termos e condições dos contratos aplicáveis que \
regem seu uso, que podem mudar de tempos em tempos. No caso de qualquer conflito, os termos fornecidos aqui \
prevalecerão. Os recursos e conteúdos fornecidos por este podem ser alterados a qualquer momento sem aviso prévio. \
Acredita-se que as informações fornecidas por este sejam confiáveis quando postadas, mas não há garantia de que elas \
sejam precisas, completas ou atuais em todos os momentos. Devido à natureza dinâmica da internet, os \
recursos que estão disponíveis gratuitamente e publicamente no bot podem exigir uma taxa ou restringir \
o acesso no dia seguinte, e a localização dos itens pode mudar à medida que menus e funcionalidades \
são reorganizados. O usuário concorda expressamente que o uso deste bot é de sua total responsabilidade. \
Nenhum material pode ser modificado, editado ou retirado de contexto, de modo que seu uso crie uma declaração \
ou impressão falsa ou enganosa sobre as posições, declarações ou ações.

<b>Condições para Produtos e Serviços</b>
Os termos e condições aplicáveis a qualquer produto, serviço ou informação serão aqueles determinados no momento \
da prestação do produto, serviço ou informação. Se você optar por acessar este bot, você o faz por iniciativa própria \
e é responsável pela conformidade com as leis locais, nacionais ou internacionais aplicáveis.

<b>Confidencialidade</b>
Trataremos todas as informações a seu respeito como confidenciais. Não divulgaremos qualquer informação \
que detenhamos sobre você, exceto nas seguintes circunstâncias: (i) sob obrigação de fazê-lo sob a lei brasileira e \
(ii) onde você forneceu sua autorização prévia por escrito para fazê-lo. Você não pode usar, exportar ou reexportar as \
informações ou qualquer cópia ou adaptação em violação de quaisquer leis ou regulamentos aplicáveis."

<b>Nenhuma Garantia</b>
Nós, desenvolvedores do bot, não fazemos quaisquer garantias, declarações, endossos ou condições, expressas ou implícitas, \
com relação ao bot ou as informações contidas nele, incluindo, sem limitação, garantias de comerciabilidade, operação, \
não infração, utilidade, integridade, precisão, atualidade, confiabilidade e adequação a uma finalidade específica. \
Além disso, não representamos ou garantimos que o bot estará disponível e atenderá aos seus requisitos, que o acesso \
será ininterrupto, que não haverá atrasos, falhas, erros, omissões ou perda de informações transmitidas, que nenhum \
vírus ou outra contaminação ou propriedades destrutivas serão transmitidas ou que nenhum dano ocorrerá no sistema do \
seu computador e/ou celular. Você é o único responsável pela proteção e backup adequados de dados e/ou equipamentos \
e por tomar precauções razoáveis e apropriadas para verificar se há vírus de computador ou outras propriedades destrutivas.

<b>Copyright Universidade Católica de Pelotas (UCPEL)</b>
Todos os textos, imagens, gráficos, animações, vídeos, músicas, sons e outros materiais \
são protegidos por direitos autorais e outros direitos de propriedade intelectual pertencentes à Universidade Católica \
de Pelotas, suas subsidiárias, afiliadas e licenciantes.

Este projeto <b>não</b> é oficialmente afiliado com a instituição de ensino Universidade Católica de Pelotas (UCPEL).

Por favor, ajude-nos a melhorar. Caso haja alguma dúvida ou sugestão, entre em contato utilizando o comando \
/desenvolvedores."""


def not_logged_in(first_name):
    return """
{}, para ter acesso a esta funcionalidade você deverá realizar o login em seu SAPU utilizando o comando \
/login [usuário] [senha].""".format(first_name)


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
{}, utilize o comando /login [usuário] [senha].""".format(first_name)


def valid_login(first_name):
    return """
{}, seu login foi efetuado com sucesso!""".format(first_name)


def wrong_password(first_name):
    return """
{}, sua senha está incorreta.""".format(first_name)


def wrong_user(first_name):
    return """
{}, seu usuário está incorreto.""".format(first_name)


def suggest_without_parameters(first_name):
    return """
{}, utilize o comando /sugerir [mensagem].""".format(first_name)


def not_registered(first_name):
    return """
{}, para ter acesso a esta funcionalidade você deverá realizar o login em seu SAPU utilizando o \ 
comando /login [usuário] [senha].""".format(first_name)


def push_grades(first_name, materia, nota, media, msg):
    return """
{}, sua nota de <b>{}</b>acabou de ser publicada no sistema!
Você tirou <b>{}</b> de 10.0.
Sua média atual é <b>{}</b>.
<b>{}</b>""".format(first_name, materia, nota, media, msg)


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
{}, você já aceitou os Termos de Uso. Digite /menu para ver o que eu posso fazer.""".format(first_name)


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
Você leu e concorda com os Termos de Uso?"""


def yes():
    return """
Você concordou com os Termos de Uso."""


def login_requirement():
    return """
Para ter acesso a todas as funcionalidades você deverá realizar o login em seu SAPU utilizando o comando /login [usuário] [senha].
Caso necessite de auxilio, digite ajuda a qualquer momento."""


def no(first_name):
    return """
{}, suas funcionalidades não estão habilitadas. Você não poderá utilizar o bot enquanto não aceitar os Termos de Uso. \
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


def help_user():
    return """
<b>Ajuda</b>

A sintaxe usada pelo telegram na execução de comandos é representada pelo uso da / seguida do comando, como mostra o exemplo a seguir:
/notas

Comandos onde são enviados parâmetros são executados da seguinte maneira:
/login parametro1 parametro2 

Preste atenção na sintaxe bibliográfica que é utilizada nos comandos onde são enviados parâmetros: 
/login [usuário] [senha]
Neste caso, o uso dos [ ] não são necessários. 

Caso você queira ver a lista completa de comandos disponíveis, utilize /comandos."""


def answer_error(first_name):
    return """
{}, ainda não consigo conversar com você de forma natural. Você pode pedir ajuda a qualquer momento caso necessite \
de auxílio.""".format(first_name)


def historico(historico):
    return """
<b>Histórico</b>

Seu histórico está disponível <a href=\"http://sapu.ucpel.edu.br/portal/{}\">aqui</a>.""".format(historico)


def boleto(first_name, boleto, option):
    if option == 1:
        return """
<b>Boleto</b>

Seu boleto está disponível <a href=\"{}\">aqui</a>.""".format(boleto)
    else:
        return """
{}, você não possui boletos em aberto.""".format(first_name)


def formata_users(telegram_id, first_name, last_name, sapu_username):
    if not last_name:
        last_name = ""
    if sapu_username == " ":
        return """
<a href="tg://user?id={}">{}</a> - {} {}""".format(telegram_id, telegram_id, first_name, last_name)
    else:
        return """
<a href="tg://user?id={}">{}</a> - <b>{} {}</b>""".format(telegram_id, telegram_id, first_name, last_name)


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
{}, utilize o comando /alert [id]** [mensagem].

**Somente números são aceitos""".format(first_name)


def statement_error(first_name):
    return """
{}, utilize o comando /statement [mensagem].""".format(first_name)


def alert_success(first_name):
    return """
{}, sua mensagem foi enviada com sucesso!""".format(first_name)


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


def push(initial, users):
    return """
{} | {}""".format(initial, users)


def developers():
    return """
<b>Desenvolvedores</b>

Este bot foi desenvolvido com muito código e café por <a href="https://t.me/lucaspeferreira">Lucas Ferreira</a> e \
<a href="https://t.me/matheuskprot">Matheus Protzen</a>."""


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

Para acessar clique <a href=\"{}\">aqui</a>.""".format(moodle)


def formata_email(de, assunto, data):
    return """
De: {}
Assunto: {}
Data: {}
""".format(de, assunto, data[:-3])


def formata_usage(func, num):
    return """
{} | {}""".format(num, func)


def speech_error(first_name):
    return """
{}, não entendi o que você falou.""".format(first_name)


def speech_request_error(first_name):
    return """
{}, não consegui processar seu audio. Que tal enviar outro?""".format(first_name)


def start_server():
    return """
<b>Comunicado</b>

O servidor foi reiniciado ou atualizado com sucesso."""


def invalid(first_name):
    return """
{}, não consigo interpretar a informação contida na mensagem que você enviou.""".format(first_name)


def unknown_command(first_name):
    return """
{}, este comando é inválido.""".format(first_name)
