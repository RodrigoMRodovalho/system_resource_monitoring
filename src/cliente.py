import socket
from threading import Thread, BoundedSemaphore
import sys
import linecache
from datetime import datetime
import time

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


# Funcao que envia mensagem para o servidor
def envia_mensagem_servidor(mensagem):
    print >> sys.stderr, 'enviando ', mensagem, '  as ', datetime.now().time()
    servidor_sock.sendall(mensagem)

# Imprime as mensagens recebidas
def log_mensagem_recebida(mensagem):
    print >> sys.stderr, 'recebido ', mensagem, '  at ', datetime.now().time()

# Funcao que guarda nas variaveis o IP e Porta do servidor
def configura_servidor(host, port):
    global host_ip, porta
    host_ip = host
    porta = port

# Funcao que conecta socket do servidor
def conecta_servidor():
    global servidor_sock
    try:
        # Cria socket para conexao
        servidor_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configura endereco - IP e Porta
        endereco_servidor = (host_ip, porta)
        print >> sys.stderr, 'Conectando em %s port %s' % endereco_servidor
        servidor_sock.connect(endereco_servidor)
        print >> sys.stderr, 'Conectado'
        return True
    except:
        return False

# Funcao que desconecta socket do servidor
def desconecta_servidor():
    servidor_sock.close()

# Funcao que realiza comunicacao com servidor
def estabelece_conexao_servidor(host_ip, porta):
    global s_servidor_contectado, servidor_conectado, mensagem_erro

    # Configura IP e Porta do Servidor
    configura_servidor(host_ip, porta)
    # Verifica se conecta com o servidor
    if (conecta_servidor()):
        # mensagem_erro = None
        # Libera a variavel que controla se conectou o servidor ou se deu erro
        s_servidor_contectado.acquire()
        servidor_conectado = True
        s_servidor_contectado.release()
    else:
        # mensagem_erro = 'Nao foi possivel conectar ao servidor'
        # Libera a variavel que controla se conectou o servidor ou se deu erro
        s_servidor_contectado.acquire()
        servidor_conectado = False
        s_servidor_contectado.release()

#Thread que escuta as mensagens vindas do servidor
def escuta_servidor():

    while True:
        data = servidor_sock.recv(4096)
        log_mensagem_recebida(data)


host_ip = '127.0.0.1'
porta = 50053
# Declaracao do socket de conexao com servidor
servidor_sock = None
servidor_conectado = False
s_servidor_contectado = BoundedSemaphore()


estabelece_conexao_servidor(host_ip, porta)
#conecta servidor
s_servidor_contectado.acquire()
if servidor_conectado:
    #executa thread para escutar as mensagens
    t = Thread(target=escuta_servidor)
    t.setDaemon(True)
    t.start()
    s_servidor_contectado.release()
    while True:
	    # le do teclado identificador do recurso
	    opcao_recurso = raw_input("Digite o recurso\n")
	    quant_recurso = raw_input("Quantidade de medicoes do recurso\n")
	    # chama funcao para imprimir informacoes coletadas do recurso pedido
	    envia_mensagem_servidor(str('recurso,127.0.0.1,'+str(opcao_recurso)+',' + str(quant_recurso) + ',0'))
else:
	print 'erro ao conectar servidor'
s_servidor_contectado.release()

