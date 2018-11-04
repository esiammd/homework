import sys #biblioteca para receber parametros passados como argumentos
import socket
import threading
from threading import Thread

lock = threading.Lock()

#ip_local = "127.0.0.1" / ip_broadcast = "192.168.1.4"
tcp_ip = "127.0.0.1"

#formato da entrada: tcp_server port_to_listen_on file_directory
#ex: python3 ./tcp_server.py 9089 ./
tcp_port = int(sys.argv[1])
tcp_directory = sys.argv[2]

#configuracoes da cache
cache = {} #cache[name][size][content]
cache_size = 0
cache_max_size = 64*1024**2 #64MB transformado em bytes
exist_in_cache = False

buffer_size = 1024  #tamanho do buffer de envio = 1024bytes = 1Kb
files = [] #lista de arquivos do server

#configuracoes do socket
s = socket.socket()
s.bind((tcp_ip, tcp_port)) #liga
s.listen(3) #escuta

#funcao que ira se comunicar com o cliente
def connection(conn, addr, lock):
    lock.acquire() #bloqueia acesso ao servidor
    global cache
    global cache_size
    global cache_max_size
    global exist_in_cache
    global buffer_size
    global files

    while True: #O servidor recebe um dado do cliente
        data = conn.recv(buffer_size).decode() #decode = funcao para decodificar, transformar de byte para string
        if data:
            if data == "listCache":
                conn.send(str(files).encode())
            else:
                print ("Client", addr, "is requesting file", data)
                if data in cache:
                    exist_in_cache = True
                    conn.send(cache[data][1])
                    print("Cache hit. File", data, "sent to the client.")
                if exist_in_cache == False:
                    try:
                        f = open(tcp_directory+data, 'rb')
                        content = f.read()
                        size_file = len(content)
                        conn.send(content)
                        if size_file > cache_max_size:
                            conn.send(content)
                            print("Cache miss. File", data, "sent to the client" )
                        else:
                            while (size_file + cache_size) > cache_max_size:
                                cache_size = cache_size - cache[files[0]][0]
                                del cache[files[0]] #remove o primeiro arquivo armazenado na cache
                                files.pop(0)
                            item = (size_file, content)
                            cache[data] = item
                            cache_size = cache_size + size_file
                            files.append(data)
                            conn.send(content)
                            print("Cache miss. File", data, "sent to the client" )
                        f.close()
                    except FileNotFoundError:
                        print("File", data, "does not exist")
                        conn.send("EOF".encode())
                else:
                    exist_in_cache = False
            lock.release() #desbloqueia acesso ao servidor
while True:
    conn, addr = s.accept() #aceita a conexao com o cliente
    Thread(target=connection, args=[conn, addr, lock]).start()
    #conn = objeto de soquete utilizavel para enviar e receber dados na conexao
    #addr = endereco ligado ao soquete na outra extremidade da conexao
