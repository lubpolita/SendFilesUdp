# Comunicação servidor/cliente UDP com implementação de janela deslizante

Este projeto é uma implementação em Python de um sistema de comunicação cliente-servidor UDP seguro com a utilização de janela deslizante. O objetivo deste trabalho é explorar os conceitos de Redes de Computadores II, especificamente protocolos de transporte UDP e janela deslizante.

O sistema é composto por dois arquivos Python: `Client.py` e `Server.py`. O arquivo `Server.py` implementa o servidor UDP que recebe os dados enviados pelo cliente. O arquivo `Client.py` implementa o cliente UDP que envia as requisições para o servidor. A implementação de janela deslizante é realizada no arquivo `Client.py`, no método "download_file" e no método "send_file" do arquivo `Server.py`.

## Requisitos

- Python 3.x
- Git

## Como usar

Certifique-se antes de instalar as bibliotecas externas `speedtest` e `ping3`. Para instalar digite os seguintes comandos no seu terminal:

```
pip install speedtest-cli
pip install ping3

```

1. Clone o repositório:

```
git clone https://github.com/lubpolita/SendFilesUdp.git
```

2. Crie uma pasta com o nome de `files` onde irá executar o `Server.py` e adicione os arquivos que você deseja ter no Servidor.

3. Execute o arquivo `Server.py` em um terminal:

```python
python3 Server.py
```

4. Modifique o arquivo `Cliente.py`, certifique-se que a variável global `IP` está configurada com o ip da máquina onde está executando o `Server.py`.

5. Execute o arquivo `Client.py` em outro terminal:

```python
python3 Client.py
```

6. Insira a senha definida em `Server.py`. Por padrão a senha será: "senha123".

7. Se você for autenticado será exibido um menu com 3 opções: listar, download e sair.
- Listar: lista todos os arquivos armazenados no servidor.
- Download: insira o nome do arquivo que deseja baixar da lista.
- Sair: sai da aplicação e encerra o socket.

O servidor enviará o arquivo para o cliente com a implementação de janela deslizante. O arquivo será recebido pelo cliente e a mensagem "O arquivo foi baixado com sucesso!" será exibida no terminal do cliente.

## Contribuições

Contribuições são bem-vindas e encorajadas. Abra uma issue para discutir as mudanças que você gostaria de fazer ou envie uma pull request.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.
