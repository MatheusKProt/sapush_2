def comandos():
    return """
<b>Lista de comandos</b>

/login [usuário] [senha] - faz o login no SAPU 
/deletar - deleta suas informações de login do SAPU 
/sugerir [mensagem] - envia uma sugestão aos desenvolvedores 

/notas - retorna suas notas do semestre atual 
/frequencia - retorna sua frequência do semestre atual 
/horarios - retorna seus horários do semestre atual 
/disciplinas - retorna suas disciplinas do semestre atual
/historico - retorna o link com seu histórico 
/curriculo - retorna todas as disciplinas do curso
/boleto - retorna o link com seu boleto em aberto 

/termos - exibe os termos de uso
/ajuda - exibe instruções de uso"""


def comandos_admin():
    return """
<b>Lista de comandos administrativos</b>

/users - exibe todos os usuários cadastrados
/alert [id] [mensagem] - envia um aviso para uma pessoa específica 
/statement [mensagem] - envia um comunicado a todos os usuários 
/sugestions - exibe todas as sugestões recebidas 

/statistics - exibe as estatísticas atuais de uso de hardware
/log - exibe o log de atualizações
/reboot - reinicia o servidor 
/update - atualiza o bot"""


def start(first_name):
    return """
Hey {}, tudo bem?

Estou aqui para lhe ajudar. Antes de mais nada, leia com atenção os Termos de Uso:

<b>Termos de Uso</b>
Pelo acesso e uso deste bot, você aceita e concorda em cumprir os termos legais de uso. Ao utilizar este bot, \
você declara que leu e compreendeu estes termos e condições e concorda em ficar vinculado aos mesmos. \
A utilização dos serviços deste bot requer obrigatória e cumulativamente (i) a realização de cadastro prévio e (ii) \
leitura e aceitação dos Termos de Uso.

Nós desenvolvedores, juntamente com o serviço prestado, não compactuamos, incentivamos ou promovemos o uso ilegal dos \
seus dados. Nosso objetivo por meio deste é facilitar a sua vida automatizando tarefas do dia a dia. \
Não assumimos qualquer responsabilidade por aqueles que utilizam estes aplicativos para qualquer outra finalidade que \
não o monitoramento próprio do Sistema de Apoio Universitário (SAPU) da Universidade Católica de Pelotas.

Caso você queira ler os Termos de Uso detalhados, selecione a opção /termos.""".format(first_name)


def termos():
    return """
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

<b>Copyright Universidade Católica de Pelotas (UCPel)</b>
Todos os direitos reservados. Todos os textos, imagens, gráficos, animações, vídeos, músicas, sons e outros materiais \
são protegidos por direitos autorais e outros direitos de propriedade intelectual pertencentes à Universidade Católica \
de Pelotas, suas subsidiárias, afiliadas e licenciantes.

Somos independentes. Não possuímos vinculo empregatício algum com a Universidade Católica de Pelotas (UCPel).

Nós valorizamos as suas opiniões. Caso haja alguma dúvida ou sugestão, entre em contato digitando o comando /sugerir [sua sugestão]."""


def not_logged_in(first_name):
    return """
{}, para ter acesso a esta funcionalidade você deverá realizar o cadastro conosco utilizando o comando \
/login [usuário] [senha].""".format(first_name)


def alert(msg):
    return """
<b>Comunicado</b>\n\n{}""".format(msg)


def invalid_login(first_name):
    return """
{}, use o comando /login [usuário] [senha].""".format(first_name)


def valid_login(first_name):
    return """
{}, seu login foi efetuado com sucesso!

Isso é tudo o que eu posso fazer:""".format(first_name)


def wrong_password(first_name):
    return """
{}, sua senha está errada.""".format(first_name)


def wrong_user(first_name):
    return """
{}, seu usuário está errado.""".format(first_name)


def suggest_without_parameters(first_name):
    return """
{}, use o comando /sugerir [mensagem].""".format(first_name)


def not_registered(first_name):
    return """
{}, para ter acesso a esta funcionalidades você deverá realizar o login em seu SAPU utilizando o \ 
comando /login [usuário] [senha].""".format(first_name)


def push_grades(first_name, materia, nota, msg):
    return """
{}, sua nota de <b>{}</b>acabou de ser publicada no sistema!
Você tirou <b>{}</b> de 10.0.
<b>{}</b>""".format(first_name, materia, nota, msg)


def push_grades_null(first_name, materia, data):
    return """
{}, sua avaliação de {} acabou de ser cadastrada no sistema e está marcada para o dia {}.

Bons estudos!""".format(first_name, materia, data)


def push_frequencia(first_name, frequencia, materia):
    return """
{}, você está com <b>{}%</b> de frequência em <b>{}</b>. 
Tome cuidado para não reprovar por frequência.""".format(first_name, frequencia, materia)


def not_allowed(first_name):
    return """
{}, esta função não está habilitada para você.""".format(first_name)


def not_agreed(first_name):
    return """
{}, esta função não está habilitada para você. Utilize o comando /acordo e siga as instruções.""".format(first_name)


def agreed(first_name):
    return """
{}, você já aceitou os Termos de Uso. Digite /comandos para ver o que eu posso fazer.""".format(first_name)


def refresh_success(first_name):
    return """
{}, seu usuário foi atualizado.""".format(first_name)


def user_doesnt_exist(first_name):
    return """
{}, você não possui cadastro para deletar.""".format(first_name)


def user_deleted(first_name):
    return """
{}, seu cadastro foi deletado com sucesso!""".format(first_name)


def not_finished(first_name):
    return """
{}, esta função não está habilitada ou está em fase de testes internos.""".format(first_name)


def do_you_agree():
    return """
Você leu e concorda com os Termos de Uso?"""


def yes(first_name):
    return """
{}, você concordou com os Termos de Uso.""".format(first_name)


def login_requirement(first_name):
    return """
{}, para ter acesso a todas as funcionalidades você deverá realizar o login em seu SAPU utilizando o comando /login [usuário] [senha].

Caso necessite de auxilio, digite ajuda a qualquer momento.""".format(first_name)


def no(first_name):
    return """
{}, suas funcionalidades não estão habilitadas. Você não poderá utilizar o bot enquanto não aceitar os Termos de Uso. \
Caso você mude de ideia, utilize o comando /acordo e siga as instruções.""".format(first_name)


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

Fique atento para a sintaxe bibliográfica utilizada nos comandos onde são enviados parâmetros: 
/login [usuário] [senha]
Neste caso, o uso dos [ ] não são necessários. 

Caso você queira ver a lista completa de comandos disponíveis, digite /comandos."""


def answer_error(first_name):
    return """
{}, ainda não consigo conversar com você naturalmente. Você pode digitar ajuda a qualquer momento caso necessite \
de auxílio.""".format(first_name)
