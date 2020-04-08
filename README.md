# homework

O HOMERWORK1 trata-se da implementação de um cliente-servidor multithread.
A implementação foi realizada em Python e está dividida em duas partes, sendo estas: SERVER e CLIENT

SERVER
O servidor recebe dois parâmetros (a porta de comunicação e o diretório dos arquivos) no seguinte formato:
./tcp_server port_to_listen_on file_directory

Em seguida liga seu socket de comunicação e fica esperando uma conexão com um client.
Quando aceita uma conexão cria uma Thread e avalia o dado de entrada conforme a descrição abaixo:

1. Se o server receber como entrada do client a mensagem "listCache" ele retorna ao client um vetor com os nomes dos arquivos armazenados na cache.
2. Se o client solicita um arquivo ao servidor, o server imprime a mensagem:
  "Client", addr, "is requesting file", data
  e inicialmente faz uma busca no srquivo na cache.
  2.1 se o arquivo solicitado se encontra na cache do servidor, o server acessa a cache, envia o arquivo ao client e imprime na tela a mensagem abaixo:
    "Cache hit. File", data, "sent to the client."
  2.2 caso não exista na cache, o server verifica se o arquivo existe em seu diretório. Em caso afirmativo ele verifica o tamanho do arquivo.
    2.2.1 se o tamanho do arquivo for maior que 64MB, ele envia o arquivo ao client e imprime a mensagem:
          "Cache miss. File", data, "sent to the client"
    2.2.2 se o tamanho do arquivo for menor que 64MB, ele verifica se é possível adicionar o arquivo na cache, isto é:
      - se tamanho da cache atual + tamanho do arquivo < 64MB:
        (a) armazena o arquivo na cache, envia o arquivo ao client e imprime a mensagem: "Cache miss. File", data, "sent to the client"
      - se tamanho da cache atual + tamanho do arquivo > 64MB:
        (b) elimina o arquivo mais antigo na cache (primeiro arquivo armazenado) e verifica novamente se é possível armazenar o arquivo na cache.
        Caso seja possível, realiza o passo (a), caso contrário, realiza novamente o passo (b)
  2.3 caso o arquivo não exista no diretório do servidor, o server imprime a mensagem:
    "File", data, "does not exist"

**OBS:** data = nome do arquivo solicitado

CLIENT
O cliente recebe quatro parâmetros (o ip do servidor, a porta de comunicação, o nome do arquivo a ser solicitado e o diretório dos arquivos) no seguinte formato:
./tcp_client server_host server_port file_name directory

Em seguida abre seu socket de comunicação e se conecta ao server.
Depois enviar uma solicitação de arquivo ou listCache ao server e recebe um dado como retorno.

1. Caso a mensagem enviada tenha sido "listCache", o client ao receber uma resposta do server imprime a mesma na tela.
2. Caso a mensagem enviada tenha sido a solicitação de um arquivo, o client abre um arquivo em seu diretório e inicia o processo de escrita, isto é, cópia do arquivo recebido.
3. Caso receba do serve a mensagem "EOF", significa que o arquivo solicitado não existe no diretório do server. Neste caso, o client imprime a mensagem:
  "file", tcp_file, "saved"

**OBS:** tcp_file = nome do arquivo solicitado
