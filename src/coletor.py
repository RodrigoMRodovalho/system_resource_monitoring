import socket
import sys
import linecache
from threading import Thread, BoundedSemaphore
from datetime import datetime
import time

COLETOR_PORTA = 50053
MONITOR_PORTA = 50999
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
    # salva o ip da maquina em arquivo
    global s_arquivo_cadastro_maquinas

    try:
        s_arquivo_cadastro_maquinas.acquire()

        # abertura do arquivo
        arquivo_maquinas_cadastradas = open(ARQUIVO_CADASTRO_MAQUINAS, 'r+')

        maquina_nao_cadastrada = True
        # verifica se a maquina ja esta cadastrada
        for maquina_ip in arquivo_maquinas_cadastradas:
            if maquina_ip == ip:
                maquina_nao_cadastrada = False
                break

        # caso a maquina nao esteja cadastrada entao escreve no arquivo
        if maquina_nao_cadastrada:
            # escrita no arquivo
            arquivo_maquinas_cadastradas.write(str(ip) + '\n')

        arquivo_maquinas_cadastradas.close()
        s_arquivo_cadastro_maquinas.release()

        return maquina_nao_cadastrada

    except:
        PrintException()
        return False


# funcao que retorna a lista de maquinas cadastradas
def lista_maquinas_cadastradas():
    # le maquinas do arquivo
    global s_arquivo_cadastro_maquinas

    # verificar se o usuario e senha estao no arquivo e se sao compativeis
    s_arquivo_cadastro_maquinas.acquire()
    arquivo_maquinas_cadastradas = open(ARQUIVO_CADASTRO_MAQUINAS, 'r')

    maquinas = ''
    # percorre o arquivo e obtem os ips das maquinas cadastradas
    for linha in arquivo_maquinas_cadastradas:
        linha = linha.replace("\n","")
        maquinas = maquinas + linha + ","

    arquivo_maquinas_cadastradas.close()
    s_arquivo_cadastro_maquinas.release()
    return maquinas


# funcao que retorna um recurso monitorado de uma maquina
def lista_recurso_maquina(conn, msg):
    # envia pedido (get) de recurso para o monitor
    socket_monitor = conecta_monitor(msg[1])
    if socket_monitor is None:
        print 'erro ao conectar'
        conn.sendall('erro ao conectar monitor')
    else:
        socket_monitor.sendall(str(msg[2] + ',' + msg[3] + ',' + msg[4]))
        resposta_monitor = socket_monitor.recv(4096)
        conn.sendall(resposta_monitor)
        desconecta_monitor(socket_monitor)


# funcao que conecta com a maquina (monitor)
def conecta_monitor(ip):
    try:
        # Cria socket para conexao
        monitor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configura endereco - IP e Porta
        endereco_servidor = (ip, MONITOR_PORTA)
        monitor_socket.connect(endereco_servidor)
        return monitor_socket
    except:
        return None


# funcao que desconecta da maquina (monitor)
def desconecta_monitor(monitor_socket):
    monitor_socket.close()


# funcao que recebe requisicao
def processa_requisicao(msg, conn, addr, numero_requisicao):
    marca_tempo = datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y - %H:%M:%S")

    print '###### Requisicao ' + numero_requisicao + ' ######'
    print '-Marca de Tempo: ' + str(marca_tempo)
    print '-Usuario\n      -IP: ' + str(addr[0]) + '\n      -PORTA: ' + str(addr[1])
    print '-Operacao:'

    if 'cadastra' in msg:
        msg = msg.split(',')
        print '      Cadastro de maquina: ' + str(msg[1])
        if cadastra_maquina(msg[1]):
            conn.sendall('Ok')
        else:
            conn.sendall('NOk')

    elif 'lista' in msg:
        print '      Listagem de maquinas cadastradas'
        conn.sendall(lista_maquinas_cadastradas())
    elif 'recurso' in msg:
        msg = msg.split(',')
        # todo imprimir
        print '      -Pedido de monitoramento:'
        print '            IP do monitor: ' + str(msg[1])
        print '            Recurso: ' + str(msg[2])
        print '            Quantidade: ' + str(msg[3])
        print '            Formato: ' + str(msg[4])
        lista_recurso_maquina(conn, msg)
    else:
        print '      Desconhecida - Erro'
        conn.sendall("Erro")
    print '######################'


# Thread que aceita as conexoes dos clientes
def aceita(conn, addr):
    global numero_usuarios_conectados, s_numero_usuarios_conectados
    global numero_requsicoes_atendidas, s_numero_requisicoes_atendidas

    s_numero_usuarios_conectados.acquire()
    numero_usuarios_conectados = numero_usuarios_conectados + 1
    s_numero_usuarios_conectados.release()

    # recebe a mensagem vinda do cliente e repassa para funcao para processar as informacoes
    while True:
        msg = conn.recv(4096)

        numero_requisicao = None
        # incrementa o numero de requisicoes atendidas
        s_numero_requisicoes_atendidas.acquire()
        numero_requisicao = str(numero_requsicoes_atendidas)
        numero_requsicoes_atendidas = numero_requsicoes_atendidas + 1
        s_numero_requisicoes_atendidas.release()

        if len(msg) == 0:
            break

        processa_requisicao(msg, conn, addr, numero_requisicao)

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

# Configuracoes de socket do servidor
HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, COLETOR_PORTA))  # liga o socket com IP e porta

print 'Rodando Coletor'

while 1:
    s.listen(1)  # espera chegar pacotes na porta especificada
    conn, addr = s.accept()  # Aceita uma conexao
    print 'Aceitou uma conexao de ', addr
    # Criacao de thread para nao travar o servidor e poder receber conexoes dos clientes a qualquer momento
    t = Thread(target=aceita, args=(conn, addr,))
    t.start()
