import socket
import threading
import random

# Configurações do servidor
servidor_endereco = 'localhost' # Endereço IP do server
servidor_porta = 1234 # Porta escolhida para estabelecer comunicação

def gera_chave():

    numeros = random.sample(range(1,51), 5) # Gera aleatóriamentre 5 numeros
    estrelas = random.sample(range(1,13), 2) # Gera aleatóriamente 2 estrelas

    # Return dos valores de numeros e estrelas
    return {'numeros': numeros, 'estrelas': estrelas}

def compara_resultados(aposta, chave):

    numeros_apostados = set(aposta['numeros'])
    estrelas_apostadas = set(aposta['estrelas'])
    numeros_vencedores = set(chave['numeros'])
    estrelas_vencedoras = set(chave['estrelas'])
    numeros_corretos = numeros_apostados.intersection(numeros_vencedores)
    estrelas_corretas = estrelas_apostadas.intersection(estrelas_vencedoras)

    # Return da validação da aposta final
    return numeros_corretos, estrelas_corretas

def conexao_com_cliente(cliente_socket):
    
    # Gera uma chave vencedora
    chave = gera_chave()

    # Aposta recebida
    aposta = cliente_socket.recv(4096).decode('utf-8')
    aposta = eval(aposta) # String passa a dicionario

    # Compara com os resultados corretos
    numeros_corretos, estrelas_corretas = compara_resultados(aposta, chave)

    # Responde ao cliente
    resposta = {'numeros_corretos': list(numeros_corretos), 'estrelas_corretas': list(estrelas_corretas)}
    cliente_socket.send(str(resposta).encode('utf-8')) # Envia resposta
    cliente_socket.close() # Fecha socket

def ligar_servidor():

    # Socket TCP é criado
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Liga socket á porta e endereço
    servidor_socket.bind((servidor_endereco, servidor_porta))

    # Socket é colocado em modo listen
    servidor_socket.listen(5)

    print("Servidor iniciado com sucesso!")

    while 1:
        cliente_socket, cliente_address = servidor_socket.accept()
        print("Conexao estabelecida com cliente:", cliente_address)

        # Nova thread é criada para lidar com o cliente
        conexao_com_cliente(cliente_socket)

ligar_servidor() # Chamada da função