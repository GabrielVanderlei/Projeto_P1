import sys
import os

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  
# Adiciona um compromisso a agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):
  '''Tarefa 9: Complete a implementação da função adicionar(), que adiciona um compromisso à agenda. Um
  compromisso tem no mínimo uma descrição. Adicionalmente, pode ter, em caráter opcional, uma data, um horário, 
  um contexto e um projeto. Esses itens opcionais são os elementos da tupla extras, o segundo parâmetro da
  função. Veja os comentários do código para saber como essa tupla é organizada. Todos os elementos dessa tupla
  precisam ser validados (com as funções definidas nas tarefas anteriores). Qualquer elemento da tupla que não passe
  pela validação deve ser ignorado.'''

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    print("Descrição em branco, não foi possível adicionar a atividade.")
    return False
  
  # data, hora, prioridade, contexto, projeto
  novaAtividade = ''
  
  if dataValida(extras[0]):
    novaAtividade += extras[0] + " "
    
  if horaValida(extras[1]):
    novaAtividade += extras[1] + " "
    
  if prioridadeValida(extras[2]):
    novaAtividade += extras[2] + " "

  novaAtividade += descricao + " "
    
  if contextoValido(extras[3]):
    novaAtividade += extras[3] + " "
    
  if projetoValido(extras[4]):
    novaAtividade += extras[4] + " "

  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
    print("Adicionado")
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  '''Tarefa 7: Implemente a função prioridadeValida(). Essa função recebe um string e verifica se ele tem exata-
  mente três caracteres, se o primeiro é ‘(’, se o terceiro é ‘)’ e se o segundo é uma letra entre A e Z. A função
  deve funcionar tanto para letras minúsculas quanto maiúsculas. Devolve True se as verificações passarem e False
  caso contrário.'''
  if len(pri) == 3:
    if pri[0] == '(' and pri[2] == ')':
      if (
        'a' <= pri[1] <= 'z' or
        'A' <= pri[1] <= 'Z' 
      ):
        return True
  return False

# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) : 
  '''Tarefa 3: Complete a implementação da função horaValida() . Essa função recebe um string e verifica se ele
  tem exatamente quatro caracteres, se tão todos dígitos, se os dois primeiros formam um número entre 00 e 23 e
  se os dois últimos formam um número inteiro entre 00 e 59. Se tudo isso for verdade, ela devolve True. Caso
  contrário, False. O arquivo já inclui uma função auxiliar para verificar se todos os caracteres de um string são
  dígitos.'''
  if len(horaMin) == 4 and soDigitos(horaMin):
    if 0 <= int(horaMin[:2]) <= 23:
      if 0 <= int(horaMin[2:]) <= 59:
        return True
  return False

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  '''Tarefa 4: Implemente a função dataValida() . Essa função recebe um string e verifica se ele tem exatamente
  oito caracteres, se tão todos dígitos e se os dois primeiros correspondem a um dia válido, se o terceiro e o quarto
  correspondem a um mês válido e se os quatro últimos correspondem a um ano válido. Sua função deve checar tam-
  bém se o dia e o mês fazem sentido juntos. Além de verificar se o mês é um número entre 1 e 12, dataValida()
  deve checar se o dia poderia ocorrer naquele mês, por exemplo, ela deve devolver False caso o dia seja 31 mas o
  mês seja 04, que tem apenas 30 dias. O ano pode ser qualquer número de 4 dígitos. Para fevereiro, considere que
  pode haver até 29 dias, sem se preocupar se o ano é bissexto ou não. Se todas as verificações passarem, a função
  devolve True. Caso contrário, False.'''
  if len(data) == 8 and soDigitos(data):
    if (
      (1 <= int(data[:2]) <= 31 and int(data[2:4]) == 1) or    
      (1 <= int(data[:2]) <= 29 and int(data[2:4]) == 2) or    
      (1 <= int(data[:2]) <= 31 and int(data[2:4]) == 3) or    
      (1 <= int(data[:2]) <= 30 and int(data[2:4]) == 4) or    
      (1 <= int(data[:2]) <= 31 and int(data[2:4]) == 5) or    
      (1 <= int(data[:2]) <= 30 and int(data[2:4]) == 6) or    
      (1 <= int(data[:2]) <= 31 and int(data[2:4]) == 7) or    
      (1 <= int(data[:2]) <= 31 and int(data[2:4]) == 8) or    
      (1 <= int(data[:2]) <= 30 and int(data[2:4]) == 9) or    
      (1 <= int(data[:2]) <= 31 and int(data[2:4]) == 10) or 
      (1 <= int(data[:2]) <= 30 and int(data[2:4]) == 11) or 
      (1 <= int(data[:2]) <= 31 and int(data[2:4]) == 12)           
    ):
      return True
  return False

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  '''Tarefa 5: Implemente a função projetoValido(). Essa função recebe um string e verifica se ele tem pelo menos
  dois caracteres e se o primeiro é ‘+’. Devolve True se as verificações passarem e False caso contrário.'''
  if len(proj) >= 2:
    if proj[0] == '+':
      return True
  return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  '''Tarefa 6: Implemente a função contextoValido(). Essa função recebe um string e verifica se ele tem pelo me-
  nos dois caracteres e se o primeiro é ‘@’. Devolve True se as verificações passarem e False caso contrário.'''
  if len(cont) >= 2:
    if cont[0] == '@':
      return True
  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  '''Tarefa 8: Complete a implementação da função organizar(). Como dito antes, essa função recebe uma lista de
  strings representando atividades e devolve uma lista de tuplas com as informações dessas atividades organizadas.'''
  itens = []
  
  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    if len(tokens) > 0:
      if dataValida(tokens[0]):
        data = tokens[0]
        tokens.pop(0)
    
    if len(tokens) > 0:
      if horaValida(tokens[0]):
        hora = tokens[0]
        tokens.pop(0)

    if len(tokens) > 0:
      if prioridadeValida(tokens[0]):
        pri = tokens[0]
        tokens.pop(0)
    
    if len(tokens) > 0:
      if projetoValido(tokens[(len(tokens)-1)]):
        projeto = tokens[(len(tokens)-1)]
        tokens.pop((len(tokens)-1))

    if len(tokens) > 0:
      if contextoValido(tokens[(len(tokens)-1)]):
        contexto = tokens[(len(tokens)-1)]
        tokens.pop((len(tokens)-1))
    
    desc = ' '.join(tokens)

    if desc != '':
      itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  '''Tarefa 11: Modifique a função listar() para ler o conteúdo do arquivo todo.txt em uma lista de strings e
  organizar esses strings em uma lista de tuplas, usando a função organizar().'''
  
  try:
    fp = open(TODO_FILE, 'r')
    conteudo = fp.read()
  except:
    print("O Arquivo ",TODO_FILE, " não existe nessa instalação.")
    return

  listaDeStrings = conteudo.split('\n')
  listaDeTuplas = organizar(listaDeStrings)
  listaOrdenada = ordenarPorPrioridade(ordenarPorDataHora(listaDeTuplas))

  '''Tarefa 14:Modifique a função listar()para que liste as atividades no 
  arquivo todo.txt. Os itens devem serlistados na ordem 
  definida anteriormente, com itens nas prioridades A-D
  aparecendo em cores e itens com priori-dadeAtambém em negrito. 
  Além disso, deve aparecer a numeração dos 
  itens, como explicado antes nesta seção,de 
  modo que possa ser usada pelas funções da próxima seção.'''
  listaComCores = colorir(listaOrdenada)
  listaComAEmNegrito = AEmNegrito(listaComCores)

  mostrarAtividades(listaComAEmNegrito)
  return 



def formatarData(data):
  return str(data[0:2])+"/"+str(data[2:4])+"/"+str(data[4:8])

def formatarHora(data):
  return str(data[0:2])+":"+str(data[2:4])

def montarAtividade(item):
  conteudoAtividade = ""

  if item[1][0] != "":
    conteudoAtividade += formatarData(item[1][0]) + " "
  if item[1][1] != "":
    conteudoAtividade += formatarHora(item[1][1]) + " "
  if item[1][2] != "":
    conteudoAtividade += item[1][2] + " "
  if item[0] != "":
    conteudoAtividade += item[0] + " "
  if item[1][3] != "":
    conteudoAtividade += item[1][3] + " "
  if item[1][4] != "":
    conteudoAtividade += item[1][4] + " "
  #conteudoAtividade += '\n'

  return conteudoAtividade

def listarContexto(contexto):
  '''Tarefa 11: Modifique a função listar() para ler o conteúdo do arquivo todo.txt em uma lista de strings e
  organizar esses strings em uma lista de tuplas, usando a função organizar().'''
  
  try:
    fp = open(TODO_FILE, 'r')
    conteudo = fp.read()
  except:
    print("O Arquivo ",TODO_FILE, " não existe nessa instalação.")
    return
  listaDeStrings = conteudo.split('\n')
  listaDeTuplas = organizar(listaDeStrings)
  listaOrdenada = ordenarPorPrioridade(ordenarPorDataHora(listaDeTuplas))

  '''contador = 0
  while contador < len(listaOrdenada):
    if listaOrdenada[contador][1][3] != contexto:
      listaOrdenada.pop(contador)
    contador += 1'''

  '''Tarefa 14:Modifique a função listar()para que liste as atividades no 
  arquivo todo.txt. Os itens devem serlistados na ordem 
  definida anteriormente, com itens nas prioridades A-D
  aparecendo em cores e itens com priori-dadeAtambém em negrito. 
  Além disso, deve aparecer a numeração dos 
  itens, como explicado antes nesta seção,de 
  modo que possa ser usada pelas funções da próxima seção.'''
  listaComCores = colorir(listaOrdenada)
  listaComAEmNegrito = AEmNegrito(listaComCores)
  listaComNumeracao = numeracao(listaComAEmNegrito)

  if(len(listaComNumeracao) == 0):
    print("Nenhuma atividade cadastrada.")
    return

  mostrarAtividadesComContexto(listaComNumeracao, contexto)
  return

def buscar(ideal):
  try:
    fp = open(TODO_FILE, 'r')
    conteudo = fp.read()
  except:
    print("O Arquivo ",TODO_FILE, " não existe nessa instalação.")
    return
  listaDeStrings = conteudo.split('\n')
  listaDeTuplas = organizar(listaDeStrings)
  listaOrdenada = ordenarPorPrioridade(ordenarPorDataHora(listaDeTuplas))

  #listaComCores = colorir(listaOrdenada)
  #listaComAEmNegrito = AEmNegrito(listaComCores)
  #listaComNumeracao = numeracao(listaComAEmNegrito)
  
  contador = 0
  emLista = 0
  for item in listaOrdenada:
    if item[0] != "":
      
      if ( 
        verify(item[1][0] == ideal[1][0],ideal[1][0]) and
        verify(item[1][1] == ideal[1][1],ideal[1][1]) and
        verify(item[1][2] == ideal[1][2],ideal[1][2]) and 
        verify(item[1][3] == ideal[1][3],ideal[1][3]) and 
        verify(item[1][4] == ideal[1][4],ideal[1][4]) and 
        contem(ideal[0], item[0])
      ):
        printAtividade(
          (str(contador + 1) + " - " + montarAtividade(
          (AEmNegrito(
            colorir([item])
            )
          )[0])), item)
        emLista += 1
    contador += 1

  if emLista == 0:
    print("Nenhuma atividade com essas configurações foi localizada.")
  return

def printAtividade(texto, item):
  if item[0] != "":  
    if item[1][2] == '(A)':
      print(BOLD + CYAN + texto + RESET + RESET)
    elif item[1][2] == '(B)':
      print(YELLOW + texto + RESET)
    elif item[1][2] == '(C)':
      print(GREEN + texto + RESET)
    elif item[1][2] == '(D)':
      print(BLUE + texto + RESET)
    else:
      print(texto)
  return


def verify(condition, value):
  if value == '':
    return True
  return condition

def contem(textoABuscar, textoOriginal):
  if textoABuscar == '':
    return True
  return textoABuscar in textoOriginal

def listarProjeto(projeto):
  try:
    fp = open(TODO_FILE, 'r')
    conteudo = fp.read()
  except:
    print("O Arquivo ",TODO_FILE, " não existe nessa instalação.")
    return
  listaDeStrings = conteudo.split('\n')
  listaDeTuplas = organizar(listaDeStrings)
  listaOrdenada = ordenarPorPrioridade(ordenarPorDataHora(listaDeTuplas))

  listaComCores = colorir(listaOrdenada)
  listaComAEmNegrito = AEmNegrito(listaComCores)
  listaComNumeracao = numeracao(listaComAEmNegrito)

  if(len(listaComNumeracao) == 0):
    print("Nenhuma atividade com o contexto exigido foi localizada.")
    return

  mostrarAtividadesComProjeto(listaComNumeracao, projeto)
  return


def mostrarAtividades(atividades):
  contador = 0
  for item in atividades:
    if item[0] != "":  
      if item[1][2] == '(A)':
        print(BOLD + CYAN + str(contador + 1) + " - " + montarAtividade(item) + RESET + RESET)
      elif item[1][2] == '(B)':
        print(YELLOW + str(contador + 1) + " - " + montarAtividade(item) + RESET)
      elif item[1][2] == '(C)':
        print(GREEN + str(contador + 1) + " - " + montarAtividade(item) + RESET)
      elif item[1][2] == '(D)':
        print(BLUE + str(contador + 1) + " - " + montarAtividade(item) + RESET)
      else:
        print(str(contador + 1) + " - " + montarAtividade(item))
    contador += 1
  return

def mostrarAtividadesComContexto(atividades, contexto):
  contador = 0
  emLista = 0
  for item in atividades:
    if item[0] != "":
      if item[1][3] == contexto:
        print(str(contador + 1) + " - " + montarAtividade(item))
        emLista += 1
    contador += 1

  if emLista == 0:
    print("Nenhuma atividade com esse contexto foi localizda.")
  return


def mostrarAtividadesComProjeto(atividades, projeto):
  contador = 0
  emLista = 0
  for item in atividades:
    if item[0] != "":
      if item[1][4] == projeto:
        print(str(contador + 1) + " - " + montarAtividade(item))
        emLista += 1
    contador += 1
    
  if emLista == 0:
    print("Nenhuma atividade com esse projeto foi localizda.")
  return

def AEmNegrito(lista):
  # Função interpretada incorretamente
  # Atualmente ela não modifica nada

  contador = 0
  while contador <= len(lista) - 1:
    prioridade = lista[contador][1][2]
    '''if lista[contador][1][2] != "":
      prioridade = BOLD+lista[contador][1][2]+RESET
    lista[contador] = (lista[contador][0], (
      lista[contador][1][0],
      lista[contador][1][1],
      prioridade,
      lista[contador][1][3],
      lista[contador][1][4]))'''
    contador += 1
  return lista

def colorir(lista):
  # Essa função foi interpretada incorretamente na hora do desenvolvimento.
  # Por isso atualmente ela não realiza nenhuma modificação
  
  contador = 0
  while contador <= len(lista) - 1:
    prioridade = lista[contador][1][2]
    '''if lista[contador][1][2] == '(A)':
      prioridade = CYAN+lista[contador][1][2]+RESET
    elif lista[contador][1][2] == '(B)':
      prioridade = YELLOW+lista[contador][1][2]+RESET
    elif lista[contador][1][2] == '(C)':
      prioridade = GREEN+lista[contador][1][2]+RESET
    elif lista[contador][1][2] == '(D)':
      prioridade = BLUE+lista[contador][1][2]+RESET'''

    lista[contador] = (lista[contador][0], (
      lista[contador][1][0],
      lista[contador][1][1],
      prioridade,
      lista[contador][1][3],
      lista[contador][1][4]))

    contador += 1
  return lista

def numeracao(lista):
  contador = 0
  while contador < len(lista) - 1:
    lista[contador] = (
      str(contador + 1) + " - " + lista[contador][0],
      (
        lista[contador][1][0],
        lista[contador][1][1],
        lista[contador][1][2],
        lista[contador][1][3],
        lista[contador][1][4]
      ))
    contador += 1
  return lista

def ordemDataHora(itens):
  # Criado pelo aluno
  # Usado em ordenarPorDataHora
  return itens[1][0] and itens[1][1]

def ordenar():
  return

def ordenarPorDataHora(itens):
  '''Tarefa 12: Construa uma função ordenarPorDataHora() que, dada uma lista de itens como a produzida por
  organizar(), com os itens já ordenados por prioridade, devolve uma lista que tem os mesmos itens, ordenados
  com base em suas datas e horas. Quanto mais antiga a data de um item, mais próximo do topo da lista o item deve
  estar. Itens que não têm data ou hora aparecem sempre no final, sem nenhuma ordem em particular. Modifique a
  função listar() que faça uso de ordenarPorDataHora().'''
  itens.sort(key=ordemDataHora, reverse=True)
  return itens
   
def ordemPrioridade(itens):
  if str(itens[1][2]) == '' :
    return '0'
  else:
    return itens[1][2]
    
def ordenarPorPrioridade(itens):
  '''Tarefa 13: Construa uma função ordenarPorPrioridade() que, dada uma lista de itens como a produzida por
  organizar(), devolve uma lista que tem os mesmos itens, ordenados com base em suas prioridades, onde itens com
  prioridades mais altas (e.g., A), aparecem antes daqueles com prioridades mais baixas (e.g., Z). Itens que não têm
  prioridade aparecem sempre no final, sem qualquer ordem particular. Sua função deve garantir que, se uma lista de
  itens já estava ordenada por data e hora, essa ordem é mantida para cada prioridade (mas não entre prioridades).
  Por exemplo, se antes a lista estava ordenada por data e havia nela os seguintes itens:
  20052017 (B)
  21052017 (A)
  22052017 (B)
  Após a execução de ordenarPorPrioridade(), a lista passaria a estar ordenada da seguinte maneira:
  21052017 (A)
  20052017 (B)
  22052017 (B)
  ou seja, o item com a prioridade A passou a aparecer primeiro mas os itens com prioridade B continuam apresentando
   a mesma ordem entre si. Modifique a função listar() que faça uso de ordenarPorPrioridade().'''
  itens.sort(key=ordemPrioridade, reverse=False)
  return itens

def fazer(num):
  '''Tarefa 20:Construa a funçãofazer()que, dados o númeroNde uma atividade, marca essa atividade comofeita. 
  Isso significa que a atividade é removida dotodo.txte movida para odone.txt.'''

  try:
    fp = open(TODO_FILE, 'r')
    conteudo = fp.read()
  except:
    print("O Arquivo ",TODO_FILE, " não existe nessa instalação.")
    return

  listaDeStrings = conteudo.split('\n')
  listaDeTuplas = organizar(listaDeStrings)
  listaOrdenada = ordenarPorPrioridade(ordenarPorDataHora(listaDeTuplas))

  if len(listaOrdenada) >= num:
    conteudoAtividade = ""

    if listaOrdenada[num - 1][1][0] != "":
      conteudoAtividade += listaOrdenada[num - 1][1][0] + " "
    if listaOrdenada[num - 1][1][1] != "":
      conteudoAtividade += listaOrdenada[num - 1][1][1] + " "
    if listaOrdenada[num - 1][1][2] != "":
      conteudoAtividade += listaOrdenada[num - 1][1][2] + " "
    if listaOrdenada[num - 1][0] != "":
      conteudoAtividade += listaOrdenada[num - 1][0] + " "
    if listaOrdenada[num - 1][1][3] != "":
      conteudoAtividade += listaOrdenada[num - 1][1][3] + " "
    if listaOrdenada[num - 1][1][4] != "":
      conteudoAtividade += listaOrdenada[num - 1][1][4] + " "
    conteudoAtividade += '\n'
  else:
    print("Atividade inexistente")
    return False

  # Escreve no ARCHIVE_FILE. 
  try: 
    try:
      fpl = open(ARCHIVE_FILE, 'r')
      content = fpl.read()

      fp = open(ARCHIVE_FILE, 'w')
      fp.write(content+conteudoAtividade)
      fp.close()
    except:
      print("O arquivo ",ARCHIVE_FILE," não existe.")
      return

    remover(num)
    print("Atividade marcada como feita.")
  
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + ARCHIVE_FILE)
    print(err)
    return False

  return True

def listarApenas(lista):
  valor = ""
  for item in lista:
    if item[1][0] != "":
      valor += item[1][0]+" "
    if item[1][1] != "":
      valor += item[1][1]+" "
    if item[1][2] != "":
      valor += item[1][2]+" "
    if item[0] != "":
      valor += item[0]+" "
    if item[1][3] != "":
      valor += item[1][3]+" "
    if item[1][4] != "":
      valor += item[1][4]+" "
    valor += '\n'
  return valor

def remover(numeroDoItem):
  '''Tarefa 16:Construa a função remover() que, dado o número de uma
   atividade, remove essa atividade do ar-quivotodo.txt. Se a atividade com 
  esse número não existir, a função deve imprimir uma mensagem de erro.'''
  
  if numeroDoItem <= 0:
    print("O id da atividade deve ser maior ou igual a 1.")
    return False

  try:
    fp = open(TODO_FILE, 'r')
    conteudo = fp.read()
  except:
    print("O arquivo ", TODO_FILE, " não foi encontrado.")
    return

  listaDeStrings = conteudo.split('\n')
  listaDeTuplas = ordenarPorPrioridade(ordenarPorDataHora(organizar(listaDeStrings)))

  try:
    listaDeTuplas.pop(numeroDoItem - 1)
  except:
    print("Essa atividade não existe.")
    return False

  conteudoReal = listarApenas(listaDeTuplas)

  try:
    fp2 = open(TODO_FILE, 'w')
    fp2.write(conteudoReal)
  except:
    print("O arquivo ", TODO_FILE, " não foi encontrado.")
    return
  #print("Deletado")
  return True

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  '''Tarefa 18:Construa a funçãopriorizar()que, dados o númeroNde uma atividade e uma prioridadeP,modifica a prioridade dessa atividadeNpara que se torne
  P. Se essa atividade já tiver outra prioridade, ela é
  sobrescrita. Se a atividade não existir, a função deve imprimir uma mensagem de erro.'''

  try:
    fp = open(TODO_FILE, 'r')
    conteudo = fp.read()
  except:
    print("O arquivo ", TODO_FILE, " não foi localizado.")
    return

  listaDeStrings = conteudo.split('\n')
  listaDeTuplas = ordenarPorPrioridade(ordenarPorDataHora(organizar(listaDeStrings)))
  
  try:
    listaDeTuplas[num - 1] = (
      listaDeTuplas[num - 1][0], #desc
      (listaDeTuplas[num - 1][1][0], #data
      listaDeTuplas[num - 1][1][1], #hora
      "("+str(prioridade).upper()+")", #pri
      listaDeTuplas[num - 1][1][3], #cont
      listaDeTuplas[num - 1][1][4]#proj
      ))
  except:
    print("Essa atividade não existe.")
    return
  
  conteudoReal = listarApenas(listaDeTuplas)

  try:
    fp2 = open(TODO_FILE, 'w')
    fp2.write(conteudoReal)
    print("Alterado")
  except:
    print("O arquivo ",TODO_FILE," não existe.")
  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    
    if len(comandos) < 3:
      print("Você não colocou a quantidade mínima de parâmetros para se adicionar uma atividade.")
      return

    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    '''Tarefa 10: Modifique a função processarComandos() para que, ao receber o comando l, invoque a função
    listar().''' 
    '''Opcional 0:Modifique seu programa para que o usuário também possa passar um critério de filtragem ao invocaro programa com o comandol. 
    Esse critério de filtragem pode ser uma prioridade, um contexto ou um projeto e o comando l
    nestes casos deve listar apenas as atividades que têm essa mesma prioridade, contexto ou projeto.'''
    if len(comandos) > 2:
      ideal = ('', ('','','','',''))
      contador = 0
      descricao = ''

      comandos.pop(0)
      comandos.pop(0)
      total = len(comandos)

      while(total > contador):
        if(dataValida(comandos[0])):
          ideal = (ideal[0], (comandos[0], ideal[1][1], ideal[1][2], ideal[1][3], ideal[1][4]))
          comandos.pop(0)
        elif(horaValida(comandos[0])):
          ideal = (ideal[0], (ideal[1][0], comandos[0], ideal[1][2], ideal[1][3], ideal[1][4]))
          comandos.pop(0)
        elif(prioridadeValida(comandos[0])):
          ideal = (ideal[0], (ideal[1][0], ideal[1][1], comandos[0].upper(), ideal[1][3], ideal[1][4]))
          comandos.pop(0)
        elif(contextoValido(comandos[len(comandos) - 1])):
          ideal = (ideal[0], (ideal[1][0], ideal[1][1], ideal[1][2], comandos[0], ideal[1][4]))
          comandos.pop(len(comandos) - 1)
        elif(projetoValido(comandos[len(comandos) - 1])):
          ideal = (ideal[0], (ideal[1][0], ideal[1][1], ideal[1][2], ideal[1][3], comandos[0]))
          comandos.pop(len(comandos) - 1)
        contador += 1
      
      if len(comandos) > 0:
        descricao = ' '.join(comandos)
        ideal = (descricao, (ideal[1][0], ideal[1][1], ideal[1][2], ideal[1][3], ideal[1][4]))

      buscar(ideal)
      return

      '''if contextoValido(comandos[2]):
        listarContexto(comandos[2])
        return
      elif projetoValido(comandos[2]):
        listarProjeto(comandos[2])
        return
      else:
        print("Contexto inválido.")
        return'''
    listar()
    return

  elif comandos[1] == REMOVER:
    '''Tarefa 15:Modifique a função processarComandos()
     para que, ao receber o comandore o número de umaatividade, invoque a função
    remover() passando esse número como parâmetro.'''
    
    if len(comandos) < 3:
      print("Você não especificou qual atividade deve ser removida.")
      return
    if remover(int(comandos[2])):
      print("Deletado")
    return    

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    '''Tarefa 19:Modifique a funçãoprocessarComandos()para que, ao receber o comandofe o número de umaatividade, invoque a função fazer()
    passando esse número como parâmetro.'''
    if len(comandos) < 3:
      print("Você não especificou qual atividade deve ser marcada como feita.")
      return
    fazer(int(comandos[2]))
    return    

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    '''Tarefa 17:Modifique a funçãoprocessarComandos()para que, ao receber o comandop, o número de uma ati-vidade
     e um caractere (maiúsculo ou minúsculo) correspondendo a uma prioridade, invoque a funçãopriorizar()
    passando esse número e esse caractere como parâmetros.'''
    if len(comandos) < 3:
      print("Você não especificou qual atividade deve ser priorizada.")
      return

    if len(comandos) < 4:
      print("Você não especificou qual o nível de prioridade da atividade.")
      return
    priorizar(int(comandos[2]), comandos[3])
    return    

    ################ COMPLETAR

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']

processarComandos(sys.argv)

def debuger(comandos):
  if comandos[1] == 'h':
    return horaValida(comandos[2])
  elif comandos[1] == 'd':
    return dataValida(comandos[2])
  elif comandos[1] == 'p':
    return prioridadeValida(comandos[2])
  elif comandos[1] == 'c':
    return contextoValido(comandos[2])
  elif comandos[1] == 'p':
    return projetoValido(comandos[2])
  elif comandos[1] == 'o':
    comandos.pop(0)
    comandos.pop(0)
    print(comandos)
    return organizar([' '.join(comandos)])
  elif comandos[1] == 'l':
    return listar()
  elif comandos[1] == 'a':
    print(comandos)
    return  processarComandos(comandos)
  

#print(debuger(sys.argv))