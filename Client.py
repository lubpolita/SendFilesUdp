import select
import socket

# Configura o endereço IP e o número de porta do servidor
# IP = "192.168.15.13"
IP = "127.0.0.1"
PORT = 1234

# Configura o tamanho do buffer de dados
BUFFER_SIZE = 1024

# Define o tamanho máximo de cada pacote
MAX_PACK_SIZE = 1024

# Define o tamanho da janela (em número de pacotes)
WINDOW_SIZE = 10

# Define o separador para que seja possível ler o número de cada pacote
SEPARATOR = "##"

# Cria um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Função que envia a senha para autenticação do servidor
def send_password(password):
    sock.sendto(("auth " + password).encode(), (IP, PORT))
    data, _ = sock.recvfrom(BUFFER_SIZE)

    if data == b"error_pass":
        print("A senha digitada está incorreta.") 
        return False
    
    return True

# Função que solicita a lista de arquivos disponíveis no servidor
def get_available_files():
    sock.sendto(b"list", (IP, PORT))

     # Espera até que o socket esteja pronto para leitura
    ready_to_read, _, _ = select.select([sock], [], [], 10.0)
    if sock in ready_to_read:
        data, _ = sock.recvfrom(BUFFER_SIZE)
        
        if data == b"error_auth":
            print("Falha na autenticação. Por favor, tente novamente.")
            return
        
        if data == b"pack_error":
            print("Ocorreu um erro durante o envio de pacotes. Tente novamente ou mais tarde. ")
            print("Ocorreu um erro. O programa será encerrado.")
            sock.close()
            exit()

        return data.decode().split("\n")
    

def teste(filename):
    sock.sendto(("download " + filename).encode(), (IP, PORT))
    
    # Espera até que o socket esteja pronto para leitura
    ready_to_read, _, _ = select.select([sock], [], [], 10.0)
    if sock in ready_to_read:
        data, _ = sock.recvfrom(BUFFER_SIZE)
        
        if data == b"error_auth":
            print("Erro de autenticação. Por favor, tente novamente")
            return
        
        if data == b"pack_error":
            print("Ocorreu um erro durante o envio de pacotes. Tente novamente ou mais tarde. ")
            return -1
        
        if data != b"ok":
            print("Verifique se o nome do arquivo está correto e tente novamente.")
            return
        
        try:
            # Cria um arquivo local para salvar o arquivo baixado
            local_filename = f"./{filename}"

            with open(local_filename, "wb") as file:
                
                expected_packet = 0
                while True:
                    # Inicializa a janela de recebimento com pacotes vazios
                    window = list(range(WINDOW_SIZE))

                    while window:
                        # Espera até que o socket esteja pronto para leitura
                        ready_to_read, _, _ = select.select([sock], [], [], 10.0)
                        if sock in ready_to_read:
                            packet, server_address = sock.recvfrom(MAX_PACK_SIZE)

                            if packet.find("FILE_COMPLETE".encode()) != -1:
                                print("O arquivo foi baixado com sucesso!")
                                file.close()
                                break
                            # Armazena número do pacote recebido
                            packet_number = int(packet.split(SEPARATOR.encode())[0])
                            print(packet_number)
                            print(expected_packet)
                            ack_packet = str(packet_number).encode()
                            sock.sendto(ack_packet, server_address) 

                            # Verifica se o número do pacote corresponde ao pacote esperado
                            if packet_number == expected_packet:
                                # Salva o pacote recebido no arquivo local e envia o ACK para o servidor
                                file.write(packet.split(SEPARATOR.encode())[1])
                                expected_packet += 1
                                window.pop(0)
                    if packet.find("FILE_COMPLETE".encode()) != -1:
                        print("O arquivo foi baixado com sucesso!")
                        break
                    
        except socket.timeout:
            message = "ERRO Tempo limite de conexão esgotado."
            print(message)
        except ConnectionRefusedError:
            message = "ERRO Conexão recusada pelo servidor."
            print(message)
        except Exception as e:
            message = f"ERRO Ocorreu um erro durante o download do arquivo: {str(e)}"
            print(message)

while True:
    # Lê a senha do usuário 
    print("Digite a senha para se conectar com o Servidor")
    password = input("> ")

    auth = send_password(password)
    
    # Não permite continuar sem senha
    if not auth:
        continue

    print("Autenticação feita com sucesso!")
    break

# Loop principal do cliente
while True:
    # Exibe o menu para o usuário
    print("Escolha uma opção:")
    print("1. Listar arquivos disponíveis no servidor")
    print("2. Baixar um arquivo")
    print("3. Sair")

    # Lê a opção escolhida pelo usuário
    option = input("> ")

    # Processa a opção escolhida pelo usuário
    if option == "1":
        files = get_available_files()

        print("Arquivos disponíveis no servidor:")
        for filename in files:
            print(filename)

    elif option == "2":
        filename = input("Digite o nome do arquivo a ser baixado: ")
        teste(filename)

    elif option == "3":
        break
    
    else:
        print("Opção inválida")

sock.close()