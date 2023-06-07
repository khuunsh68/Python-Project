import socket

# Configurações do cliente
cliente_endereco = 'localhost' # Endereço IP do cliente
cliente_porta = 1234 # Porta do cliente para comunicação

def enviar_aposta(aposta):

    # Socket TCP é criado
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conexão com o servidor
    cliente_socket.connect((cliente_endereco, cliente_porta))

    # Envio da aposta para o servidor
    cliente_socket.send(str(aposta).encode('utf-8'))

    # Resposta do servidor com os resultados do jogo
    resposta = cliente_socket.recv(4096).decode('utf-8')
    resposta = eval(resposta) # String convertida para dicionario

    # Resultados imprimidos
    print("Numeros certos:", resposta['numeros_corretos'])
    print("Estrelas certas:", resposta['estrelas_corretas'])

    # Conexão com servidor fechada
    cliente_socket.close()

aposta = {'numeros': [1,2,3,4,5], 'estrelas': [6,7]} # Aposta feita
enviar_aposta(aposta)