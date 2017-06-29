import socket
import sys
import linecache
from threading import Thread, BoundedSemaphore
from datetime import datetime, timedelta
import time


COLETOR_PORTA = 50053
ARQUIVO_CADASTRO_MAQUINAS = "maquinas.txt"

###Soluca da internet para ver todas as informacoes sobre o erro dentro do except:
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

# funcao que cadastra uma maquina
def cadastra_maquina(ip):
	#salva o ip da maquina em arquivo
	global s_arquivo_cadastro_maquinas

    s_arquivo_cadastro_maquinas.acquire()

    #abertura do arquivo
    arquivo_maquinas_cadastradas = open(ARQUIVO_CADASTRO_MAQUINAS, 'r+')

    #escrita no arquivo
    arquivo_maquinas_cadastradas.write(str(ip) + '\n')
        
    arquivo_maquinas_cadastradas.close()
    s_arquivo_cadastro_maquinas.release()

# funcao que retorna a lista de maquinas cadastradas
def lista_maquinas_cadastradas():
	#le maquinas do arquivo
	global s_arquivo_cadastro_maquinas

    # verificar se o usuario e senha estao no arquivo e se sao compativeis
    s_arquivo_cadastro_maquinas.acquire()
    arquivo_maquinas_cadastradas = open(ARQUIVO_CADASTRO_MAQUINAS, 'r')
    
    maquinas = ''
    #percorre o arquivo e obtem os ips das maquinas cadastradas
    for linha in arquivo_maquinas_cadastradas:
        maquinas = maquinas + ','
    
    arquivo_maquinas_cadastradas.close()
    s_arquivo_cadastro_maquinas.release()

# funcao que retorna um recurso monitorado de uma maquina
def lista_recurso_maquina(ip,recurso,formato):
	#envia pedido (get) de recurso para o monitor
	pass

# funcao que imprime informacoes da requisicao feita pelo usuario
def imprime_requisicao():
	#IP DO USUARIO
	#PORTA DO USUARIO
	#INFORMACOES DA REQUISICAO (IP MAQUINA, RECURSO, FORMATO)
	#TIMESTAMP
	pass

# funcao que conecta com a maquina (monitor)
def conecta_monitor(ip):
	pass

# funcao que desconecta da maquina (monitor)
def desconecta_monitor(ip):
	pass

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

        #verifica o tipo da mensagem para processar
        if 'Contato_cliente' in data:
            #executa o metodo para mostrar janela de contato do cliente  na thread da interface grafica
            wx.CallAfter(tela.mostra_comprador,str(data))
        elif 'Contato_vendedor' in data:
            # executa o metodo para mostrar janela de contato do vendedor na thread da interface grafica
            wx.CallAfter(tela.mostra_vendedor,str(data))
        elif 'Lance' in data:
            # chama funcao para atualizar o lance na tabela de leiloes
            tela.atualiza_leilao_tabela(str(data))
        elif 'Fim_leilao' in data:
            # executa o metodo para mostrar janela de aviso de fim de leilao na thread da interface grafica
            wx.CallAfter(tela.mostra_fim_leilao,str(data))
        elif 'Listagem' in data:
            # executa o metodo para mostrar janela da lista de leiloes na thread da interface grafica
            wx.CallAfter(tela.mostra_lista_leiloes,str(data))
        else:
            # executa o metodo para processar as respostas de Ok e not_okna thread da interface grafica
            wx.CallAfter(tela.processa_resposta, str(data))


# funcao que recebe requisicao
def processa_requisicao(msg,conn,addr,numero_requisicao):
	
	marca_tempo = datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y - %H:%M:%S.%f")

	print '###### Requisicao ' + numero_requisicao + ' ######'
	print 'Marca de Tempo: ' + str(marca_tempo)
	print 'Usuario\n      IP: ' + addr + '\n      PORTA: ' + addr
	print 'Opercacao:'

	if 'cadastra' in msg:
		#todo imprimir
		pass
	elif 'lista' in msg:
		#todo imprimir
		pass
	elif 'recurso' in msg:
		#todo imprimir
		pass
	else
		#todo imprimir
		conn.sendAll("Erro")

#Thread que aceita as conexoes dos clientes
def aceita(conn,addr):
    global numero_usuarios_conectados,s_numero_usuarios_conectados
    global numero_requsicoes_atendidas,s_numero_requisicoes_atendidas

    s_numero_usuarios_conectados.acquire()
    numero_usuarios_conectados = numero_usuarios_conectados + 1
    s_numero_usuarios_conectados.release()
    
    #recebe a mensagem vinda do cliente e repassa para funcao para processar as informacoes
    while True:
        msg = conn.recv(4096)

        numero_requisicao = None
        #incrementa o numero de requisicoes atendidas
        s_numero_requisicoes_atendidas.acquire()
        numero_requisicao = str(numero_requsicoes_atendidas)
        numero_requsicoes_atendidas = numero_requsicoes_atendidas + 1
        s_numero_requisicoes_atendidas.release()

        if len(msg) == 0:
            break

        processa_requisicao(msg, conn, addr,numero_requisicao)

    print 'conexao encerrada ', addr
    s_numero_usuarios_conectados.acquire()
    numero_usuarios_conectados = numero_usuarios_conectados - 1
    s_numero_usuarios_conectados.release()
    conn.close()

# contador do numero de usuarios conectados e um semaforo para controle
numero_usuarios_conectados = 0
s_numero_usuarios_conectados = BoundedSemaphore()

# contador do nunero de requisicoes atendidas e um semaforo para controle
numero_requsicoes_atendidas = 0
s_numero_requisicoes_atendidas = BoundedSemaphore()

# semaforo de controle para acesso ao arquivo de cadastro de maquinas
s_arquivo_cadastro_maquinas = BoundedSemaphore()

# estrutura para guardar os usuarios conectados
usuarios_conectados = {}
# semaforo de controle para estrutura de usuarios conectados
s_usuarios_conectados = BoundedSemaphore()

# TODO- Criar socket servidor
# TODO - Criar socket clientecbv

#Configuracoes de socket do servidor
HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, COLETOR_PORTA))  # liga o socket com IP e porta

while 1:
    s.listen(1)  # espera chegar pacotes na porta especificada
    conn, addr = s.accept()  # Aceita uma conexao
    print 'Aceitou uma conexao de ', addr
    #Criacao de thread para nao travar o servidor e poder receber conexoes dos clientes a qualquer momento
    t = Thread(target=aceita, args=(conn,addr,))
    t.start()








