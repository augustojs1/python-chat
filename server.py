import threading
import socket

host = '172.22.208.1' #localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} se desconectou!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Conectou-se com o endereço {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'O nickname do usuario e {nickname}!')
        broadcast(f'{nickname} se conectou ao chat!'.encode('ascii'))
        client.send('Conectado ao servidor'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Servidor online...")
receive()