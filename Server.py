import select
import socket
import os
import time

# Configura o endereço IP e o número de porta do servidor
IP = ""
PORT = 1234

# Cria um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Liga o socket ao endereço IP e porta
sock.bind((IP, PORT))

# Define a senha
PASSWORD = "senha123"

# Configura o tamanho do buffer de dados
BUFFER_SIZE = 1024

# Define o tamanho máximo de cada pacote
MAX_PACK_SIZE = 512

# Configura a pasta onde os arquivos estão armazenados
FILES_DIR = "files/"

# Define o tamanho da janela (em número de pacotes)
WINDOW_SIZE = 10

# Cria uma lista de arquivos disponíveis no servidor
available_files = os.listdir(FILES_DIR)

class Authentication:
    def __init__(self, auth):
        self.authenticated = auth

def teste(filename, client_address):
    file_path = os.path.join(FILES_DIR, filename)

    # Abre o arquivo para leitura em modo binário
    with open(file_path, 'rb') as file:
        # Inicializa a janela
        window = [file.read(MAX_PACK_SIZE) for i in range(WINDOW_SIZE)]
       
        packet_number = 0
        exp_ack = 0
        separator = "##"
        
        file.seek(0)
        while True:
            window.clear()
            count_valid_packs = 0
            # Preenche a janela
            for i in range(WINDOW_SIZE):
                pack = (file.read(MAX_PACK_SIZE))
                if pack:
                    count_valid_packs += 1
                window.append(pack)
                
            if count_valid_packs == 0:
                break

            # Envio da janela
            for packet in window:
                # Adiciona o número do pacote ao início do pacote
                packet = str(packet_number).encode() + separator.encode() + packet
                        
                # Envia o pacote para o cliente
                sock.sendto(packet, client_address)
                time.sleep(0.02)

                # Aguarda o ACK do cliente
                sock.settimeout(2)

                try:
                    # Espera até que o socket esteja pronto para leitura
                    ready_to_read, _, _ = select.select([sock], [], [], 3.0)
                    if sock in ready_to_read:
                        time.sleep(0.02) # aguarda instantes para o cliente confirmar

                        # Recebe ACK do cliente
                        ack_packet, _ = sock.recvfrom(MAX_PACK_SIZE)
                        ack_number = int(ack_packet)

                        # print(ack_number)
                        # print(exp_ack)
                        
                        while ack_number != exp_ack:
                            # Envia novamente o pacote com erro
                            sock.sendto(packet, client_address)
                            time.sleep(0.02)
                        
                            # Espera até que o socket esteja pronto para leitura
                            ready_to_read, _, _ = select.select([sock], [], [], 3.0)
                            if sock in ready_to_read:
                                ack_packet, _ = sock.recvfrom(MAX_PACK_SIZE)
                                ack_number = int(ack_packet)
                        
                        exp_ack += 1
                        packet_number += 1

                except socket.timeout:
                    # Envia novamente o pacote com erro caso timeout
                    sock.sendto(packet, client_address)
                    time.sleep(0.02)

        sock.sendto(b"##FILE_COMPLETE", client_address)
        print("Arquivo enviado com sucesso.")
        sock.settimeout(0)
        
def menu_control(auth):
    password = ''

    # Espera por uma conexão
    print('Esperando por uma conexão...')

    # Recebe a mensagem do cliente
    data, client_address = sock.recvfrom(BUFFER_SIZE)
    print('Conexão recebida de', client_address)

    # Se a mensagem for uma solicitação de lista de arquivos, envia a lista para o cliente
    if data == b"list":
        if not auth.authenticated: 
            sock.sendto(b"error_auth", client_address) 
            return

        message = "\n".join(available_files)
        sock.sendto(message.encode(), client_address)

    # Se a mensagem for uma solicitação de download, envia o arquivo correspondente para o cliente
    elif data.startswith(b"download "):
        if not auth.authenticated: 
            sock.sendto(b"error_auth", client_address)
            
            return

        filename = data.split()[1].decode()
        if filename in available_files:
            sock.sendto(b"ok", client_address)
            teste(filename, client_address)
            print('arq enviado')
        
        else:
            sock.sendto(b"error", client_address)

    elif data.startswith(b"auth "):
        password = data.split()[1].decode()

        if password != PASSWORD:
            sock.sendto(b"error_pass", client_address)
            auth.authenticated = False
            return

        auth.authenticated = True
        sock.sendto(b"sucess_pass", client_address)


authentication = Authentication(False)

menu_control(authentication)
# Loop principal do servidor
while True:
    # Cria um socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Liga o socket ao endereço IP e porta
    sock.bind((IP, PORT))

    # Espera até que o socket esteja pronto para leitura
    ready_to_read, _, _ = select.select([sock], [], [], 10.0)
    if sock in ready_to_read:
        menu_control(authentication)
        sock.close()

