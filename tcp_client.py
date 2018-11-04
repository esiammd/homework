import sys #biblioteca para receber parametros passados como argumentos
import socket
import select

#formato da entrada: tcp_client server_host server_port file_name directory
#ex: python3 ./tcp_client.py 127.0.0.1 9089 homework1.html ./
tcp_ip = sys.argv[1]
tcp_port = int(sys.argv[2])
tcp_file = sys.argv[3]
tcp_directory = sys.argv[4]

#funcao que permite o cliente obter os nomes dos arquivos no cache do servidor
def list():
    s.send("listCache".encode())
    dataList = s.recv(buffer_size)
    print(dataList)

buffer_size = 1024 #tamanho do buffer de envio = 1024bytes = 1Kb

#configurações do socket
s = socket.socket()
s.connect((tcp_ip, tcp_port)) #O cliente se conecta ao servidor

s.send(tcp_file.encode()) #O cliente envia solicitacao de um arquivo ou listCache
data = s.recv(buffer_size)
if tcp_file == "listCache":
    print(data)
else:
    if data == "EOF".encode():
        print("file", tcp_file, "does not exist in the server")
    else:
        f = open(tcp_directory+tcp_file,'wb')
        f.write(data)
        while (select.select([s],[],[],0.1)[0]): #devolve um array dos elementos prontos, entre os 3 arrays.
        #Onde o primeiro eh para leitura, o segundo para escrita e o terceiro para execucao.O ultimo parametro eh o timeout em segundos.
        #Quando nao ha mais o que ler, o select devolve uma lista vazia e sai do loop.
            data = s.recv(buffer_size) #tamanho dos blocos, recebe no tamanho de 1Ks
            f.write(data)
        print("file", tcp_file, "saved")
        f.close()
s.close()
