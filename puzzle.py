import time
import sys

# classe que representa os nós
class Estado:
    def __init__(self, estado, pai, movimento, custo, profundidade):
        self.estado = estado
        self.pai = pai
        self.movimento = movimento
        self.custo = custo
        self.profundidade = profundidade

        if self.estado:
            self.mapa = ''.join(str(e) for e in self.estado)

    def __eq__(self, other):
        return self.mapa == other.mapa

    def __lt__(self, other):
        return self.mapa < other.mapa

nosExpandidos = 0  # contador da expansão de nos
profundidadeMax = 0  # contador da profundidade maxima
bordaMax = 0  # contador da borda maxima
bordaTam = 0  # contador da borda


def bfs(estadoInicial):
    global profundidadeMax, bordaMax, bordaTam
    start_time = time.time()  # inicia o cronometro
    estadoObjetivo = [0, 1, 2, 3, 4, 5,  6, 7, 8]  # definiçao de como deve ser o estado final do 8puzzle
    explorado = set()  # usando set() para evitar que entrem elementos repetidos
    fila = list()
    fila.append(Estado(estadoInicial, None, None, 0, 0))  # criacao do no inicial

    while fila:
        no = fila.pop(0)
        explorado.add(no.mapa)

        if no.estado == estadoObjetivo:  # retorna o no em que a solucao eh encontrada
            lerCaminho(no)
            print('nos expandidos: ', nosExpandidos, '\ntamanho da borda: ', bordaTam, '\ntamanho max da borda: ',
                  bordaMax, '\nprofundidade da busca: ', no.profundidade, '\nprofundidade maxima: ', profundidadeMax)
            print('tempo de execução: ', time.time()-start_time, 'segundos')
            return no

        vizinhos = expandir(no)  # cria uma lista com os nos vizinhos
        for vizinho in vizinhos:
            if vizinho.mapa not in explorado:  # verifica se o no ja foi usado
                fila.append(vizinho)
                explorado.add(vizinho.mapa)

                if vizinho.profundidade > profundidadeMax:
                    profundidadeMax += 1
        bordaTam = len(fila)
        if len(fila) > bordaMax:
            bordaMax = len(fila)


def dfs(estadoInicial):
    global profundidadeMax, bordaMax, bordaTam
    start_time = time.time()  # inicia o cronometro
    estadoObjetivo = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # definiçao de como deve ser o estado final do 8puzzle
    explorado = set()  # usando set() para evitar que entrem elementos repetidos
    pilha = list()
    pilha.append(Estado(estadoInicial, None, None, 0, 0))  # criacao do no inicial

    while pilha:
        no = pilha.pop()
        explorado.add(no.mapa)

        if no.estado == estadoObjetivo:
            lerCaminho(no)
            print('nos expandidos: ', nosExpandidos, '\ntamanho da borda: ', bordaTam, '\ntamanho max da borda: ',
                  bordaMax, '\nprofundidade da busca: ', no.profundidade, '\nprofundidade maxima: ', profundidadeMax)
            print('tempo de execução: ', time.time() - start_time, 'segundos')
            return no

        vizinhos = reversed(expandir(no))
        for vizinho in vizinhos:
            if vizinho.mapa not in explorado:  # verifica se o no ja foi usado
                pilha.append(vizinho)
                explorado.add(vizinho.mapa)

                if vizinho.profundidade > profundidadeMax:
                    profundidadeMax += 1
        bordaTam = len(pilha)
        if len(pilha) > bordaMax:
            bordaMax = len(pilha)


def dls(estadoInicial, fundo):
    global profundidadeMax, bordaMax, bordaTam
    start_time = time.time()  # inicia o cronometro
    estadoObjetivo = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # definiçao de como deve ser o estado final do 8puzzle
    explorado = set()  # usando set() para evitar que entrem elementos repetidos
    pilha = list()
    pilha.append(Estado(estadoInicial, None, None, 0, 0))  # criacao do no inicial
    trava = 0  # variavel que vai servir pra limitar a quantidade de iterações

    while pilha:

        no = pilha.pop()
        explorado.add(no.mapa)

        if no.estado == estadoObjetivo:
            lerCaminho(no)
            print('nos expandidos: ', nosExpandidos, '\ntamanho da borda: ', bordaTam, '\ntamanho max da borda: ',
                  bordaMax, '\nprofundidade da busca: ', no.profundidade, '\nprofundidade maxima: ', profundidadeMax)
            print('tempo de execução: ', time.time() - start_time, 'segundos')
            return False

        elif no.profundidade <= fundo:
            vizinhos = reversed(expandir(no))
            for vizinho in vizinhos:
                if vizinho.mapa not in explorado:  # verifica se o no ja foi usado
                    pilha.append(vizinho)
                    explorado.add(vizinho.mapa)

                    if vizinho.profundidade > profundidadeMax:
                        profundidadeMax += 1
            bordaTam = len(pilha)
            if len(pilha) > bordaMax:
                bordaMax = len(pilha)
    return True


def idfs(estadoInicial):
    a = True
    b = 0
    while a:
       a = dls(estadoInicial, b)
       b += 1


def expandir(no):
    global nosExpandidos
    nosExpandidos += 1

    vizinhos = list()  # inicializa a lista de nos vizinhos

    vizinhos.append(Estado(mover(no.estado, 1), no, 1, no.profundidade + 1, no.custo + 1))
    vizinhos.append(Estado(mover(no.estado, 2), no, 2, no.profundidade + 1, no.custo + 1))
    vizinhos.append(Estado(mover(no.estado, 3), no, 3, no.profundidade + 1, no.custo + 1))
    vizinhos.append(Estado(mover(no.estado, 4), no, 4, no.profundidade + 1, no.custo + 1))

    nos = list()
    for i in range(4):  # adiciona apenas os nos que levam a estados validos
        if vizinhos[i].estado is None:
            pass
        else:
            nos.append(vizinhos[i])

    return nos


def mover(estado, posicao):
    novoEstado = estado[:]  # cria copia do estado
    indice = novoEstado.index(0)

    cima = [0, 1, 2]
    baixo = [6, 7, 8]
    esquerda = [0, 3, 6]
    direita = [2, 5, 8]

    if posicao == 1:  # movimenta o 0 pra cima
        if indice not in cima:
            aux = novoEstado[indice - 3]
            novoEstado[indice - 3] = novoEstado[indice]
            novoEstado[indice] = aux

            return novoEstado
        else:
            return None

    if posicao == 2:  # movimenta o 0 pra baixo
        if indice not in baixo:
            aux = novoEstado[indice + 3]
            novoEstado[indice + 3] = novoEstado[indice]
            novoEstado[indice] = aux
            return novoEstado
        else:
            return None

    if posicao == 3:  # movimenta o 0 pra esquerda
        if indice not in esquerda:
            aux = novoEstado[indice - 1]
            novoEstado[indice - 1] = novoEstado[indice]
            novoEstado[indice] = aux
            return novoEstado
        else:
            return None

    if posicao == 4:  # movimenta o 0 pra direita
        if indice not in direita:
            aux = novoEstado[indice + 1]
            novoEstado[indice + 1] = novoEstado[indice]
            novoEstado[indice] = aux
            return novoEstado
        else:
            return None


def lerCaminho(estado):
    caminho = list()
    a = estado
    b = 1
    while b:
        if a.movimento == 1:
            caminho.append('cima')
        elif a.movimento == 2:
            caminho.append('baixo')
        elif a.movimento == 3:
            caminho.append('esquerda')
        elif a.movimento == 4:
            caminho.append('direita')
        elif a.pai is None:
            b = 0
        a = a.pai
    caminho.reverse()
    print('caminho: ', caminho)
    print('custo do caminho: ', len(caminho))



a = list()
b = sys.argv[2]

for i in range(0, 17):
    if b[i] == '1':
        a.append(1)
    if b[i] == '2':
        a.append(2)
    if b[i] == '3':
        a.append(3)
    if b[i] == '4':
        a.append(4)
    if b[i] == '5':
        a.append(5)
    if b[i] == '6':
        a.append(6)
    if b[i] == '7':
        a.append(7)
    if b[i] == '8':
        a.append(8)
    if b[i] == '9':
        a.append(9)
    if b[i] == '0':
        a.append(0)

c = sys.argv[1]
if c == 'bfs':
    bfs(a)
if c == 'dfs':
    dfs(a)
if c == 'idfs':
    idfs(a)
