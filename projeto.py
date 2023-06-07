import random
import multiprocessing as mp
import queue
import threading
import time # Falta colocar o time a funcionar

# Configuração do número de jogadores no servidor
numJogadores = 20
# Implementação do JackPot
jackPot = 1000000 # Prémio de 1 Milhão

# Função que vai gerar uma chave aleatória
def geraChave():
    numeros = random.sample(range(1, 51), 5) # Gera aleatóriamente 5 números
    estrelas = random.sample(range(1, 13), 2) # Gera aleatóriamente 2 estrelas
    return {'numeros': numeros, 'estrelas': estrelas}

# Função que compara os resultados entre aposta feita e chave correta
def comparaResultados(aposta, chave):
    numerosApostados = set(aposta['numeros'])
    estrelasApostadas = set(aposta['estrelas'])
    numerosChave = set(chave['numeros'])
    estrelasChave = set(chave['estrelas'])
    numerosCorretos = sorted(list(numerosApostados.intersection(numerosChave)))
    estrelasCorretas = sorted(list(estrelasApostadas.intersection(estrelasChave)))
    return numerosCorretos, estrelasCorretas

# Função que verifica se jogador ganhou ou não jackPot
def verificacaoJackPot(resultado, chave):
    return resultado['numerosCorretos'] == sorted(chave['numeros']) and resultado['estrelasCorretas'] == sorted(chave['estrelas'])

# Função que implementa a lógica do cliente
def cliente(aposta, resultados, chave):
    numerosCorretos, estrelasCorretas = comparaResultados(aposta, chave)
    vencedor = verificacaoJackPot({'numerosCorretos': numerosCorretos, 'estrelasCorretas': estrelasCorretas}, chave)
    resultado = {'numerosCorretos': numerosCorretos, 'estrelasCorretas': estrelasCorretas, 'chave': chave, 'vencedor': vencedor}
    resultados.put(resultado)

    # Cria um ficheiro de log caso ainda não exista e regista as apostas feitas
    file = open('cliente_log.txt', 'a')
    file.write(f"\nAposta: {aposta}\n")
    file.close()

# Função que faz o processamento das apostas
def processamentoApostas(apostas, resultados, chave):
    while not apostas.empty():
        aposta = apostas.get()
        cliente(aposta, resultados, chave)
        apostas.task_done()


# Função que implementa a lógica do servidor
def servidor():
    resultados = queue.Queue() # Queue cria uma fila compartilhada que serve para armazenar resultados
    apostas = queue.Queue() # fila compartilhada para armazenar apostas
    threads = []

    # Gera uma chave única com os resultados certos
    chave = geraChave()

    for jogador in range (numJogadores): # () serve para passar numJogadores como argumento para a função 'range'
        # Simulação de uma aposta vencedora do jackPot como teste da funcionalidade
        if jogador == 0:
            aposta = chave # Aposta feita igual à chave
        else:
            # Para os restantes jogadores são feitas apostas ao calhas
            aposta = {'numeros': random.sample(range(1, 51), 5), 'estrelas': random.sample(range(1, 13), 2)}

        apostas.put(aposta) # Aposta adicionada à lista de apostas
        t = threading.Thread(target=processamentoApostas, args=(apostas, resultados, chave))
        t.start()
        threads.append(t)

    apostas.join()

    # Print da chave correta
    print("Chave:", chave)
    print("Recibos gerados!")

    jogador = 1 # Inicialização da variável jogador a ser usada a seguir
    file = open('servidor_log.txt', 'w') # Ficheiro de log do servidor é aberto em modo escritura
    # Enquanto existirem resultados, vão ser todos guardados para cada jogador
    while not resultados.empty():
        resultado = resultados.get()
        file.write(f"\n<--- Jogador {jogador} --->\n")
        file.write(f"Numeros corretos: {resultado['numerosCorretos']}\n")
        file.write(f"Estrelas corretas: {resultado['estrelasCorretas']}\n")

        # Caso o jogador ganhe o jackpot
        if resultado['vencedor']:
            file.write(f"Vencedor do JackPot no valor de: {jackPot}\n")

        jogador += 1 # Variável jogador é incrementada até que o loop termine
    file.close()

# Inicializa servidor
servidor()