# imorta biblioteca que coleta as informacoes do sistema
import psutil
# importa estrutura para fazer a janela deslizante
from collections import deque
import time
from threading import Thread
import copy
import datetime

PORT = 50999

# identificadores para cada recurso
COLETA_CPU = 0
COLETA_MEMORIA = 1
COLETA_SWAP = 2
COLETA_REDE = 3
COLETA_NUM_PROCESSOS_ATIVOS = 4
COLETA_MAX_PROC_MEM = 5
COLETA_MAX_PROC_CPU = 6
COLETA_DISCO = 7


# Classe que representa os recursos da maquina
class Recursos:
    def __init__(self):
        self.tempo = time.time()
        self.cpu = None
        self.memoria = None
        self.swap = None
        self.rede = None
        self.num_processos_ativos = None
        self.cinco_processos_mem = None
        self.cinco_processos_cpu = None
        self.disco = None

    # imprime as informacoes dos recursos
    def __str__(self):
        print self.formata_tempo()
        print self.cpu
        print self.memoria
        print self.swap
        print self.rede
        print 'Numero de Processos ativos: ' + str(self.num_processos_ativos)
        print self.cinco_processos_mem
        print self.cinco_processos_cpu
        print self.disco
        return ''

    # formata timestamp em data
    def formata_tempo(self):
        return datetime.datetime.fromtimestamp(self.tempo).strftime("%d/%m/%Y - %H:%M:%S.%f")

    # Salva dado de cpu
    def registra_cpu(self, cpu):
        self.cpu = cpu

    # Salva dado de memoria
    def registra_memoria(self, memoria):
        self.memoria = memoria

    # Salva dado de memoria swap
    def registra_swap(self, swap):
        self.swap = swap

    # Salva dado de rede
    def registra_rede(self, rede):
        self.rede = rede

    # Salva quantidade de processos ativos
    def registra_num_proc_ativos(self, num_proc_ativos):
        self.num_processos_ativos = num_proc_ativos

    # Salva dado dos 5 processos que mais consomem memoria
    def registra_cinco_proc_mem(self, proc_mem):
        self.cinco_processos_mem = proc_mem

    # Salva dado dos 5 processos que mais consomem cpu
    def registra_cinco_proc_cpu(self, proc_cpu):
        self.cinco_processos_cpu = proc_cpu

    # Salva dado de disco
    def registra_disco(self, disco):
        self.disco = disco


# Classe que representa a memoria virtual
class Memoria:
    def __init__(self, mb, porcento):
        self.mb = mb
        self.porcento = porcento

    # imprimi informacoes de memoria virtual
    def __str__(self):
        print 'Memoria Virtual : '
        print '                : ' + str(self.mb) + ' MB'
        print '                : ' + str(self.porcento) + ' %'
        return ''


# Classe que representa a memoria swap
class MemoriaSwap:
    def __init__(self, mb, porcento):
        self.mb = mb
        self.porcento = porcento

    # imprimi informacoes de memoria swap
    def __str__(self):
        print 'Memoria Swap : '
        print '             : ' + str(self.mb) + ' MB'
        print '             : ' + str(self.porcento) + ' %'
        return ''


# Classe que representa a memoria cpu
class Cpu:
    def __init__(self, porcento):
        self.porcento = porcento

    # imprimi informacoes de memoria
    def __str__(self):
        print 'CPU : '
        print '    : ' + str(self.porcento) + ' %'
        return ''


# Classe que representa as informacoes das interfaces de rede
class Rede:
    def __init__(self):
        self.rede = {}

    # Registra interface e seus dados de trafego
    def insere_interface(self, interface, pacotes_enviados, pacotes_recebidos):
        self.rede[interface] = [pacotes_enviados, pacotes_recebidos]

    # imprimi informacoes de rede
    def __str__(self):
        print 'Rede : '
        for interface in self.rede:
            print '        Interface : ' + str(interface)
            print '                  : Pacotes Enviados : ' + str(self.rede[interface][0])
            print '                  : Pacotes Recebidos: ' + str(self.rede[interface][1])
        return ''


# Classe que representa as informacoes de um processo
class Processo:
    def __init__(self, pid, nome, dono, tempo, mem, cpu):
        self.pid = pid
        self.nome = nome
        self.dono = dono
        self.tempo = tempo
        self.mem = mem
        self.cpu = cpu

    # imprimi informacoes do processo
    def __str__(self):
        print '      PID ' + str(self.pid)
        print '      Nome ' + str(self.nome)
        print '      Dono ' + str(self.dono)
        print '      Tempo ' + str(self.tempo)
        print '      Consumo de memoria ' + str(self.mem) + '%'
        print '      Consumo de cpu ' + str(self.cpu) + '%'
        return ''


# Classe que represente a lista dos processos que mais consomem memoria
class ProcessosMaxMemoria:
    def __init__(self):
        self.proc = {}

    # registra processo
    def adiciona_processo(self, processo):
        self.proc[processo] = processo

    # imprime os processos que mais consomem memoria
    def __str__(self):
        print 'Processos - Maior Consumo Memoria'
        for p in self.proc:
            print p
        return ''


# Classe que represente a lista dos processos que mais consomem cpu
class ProcessosMaxCpu:
    def __init__(self):
        self.proc = {}

    # registra processo
    def adiciona_processo(self, processo):
        self.proc[processo] = processo

    # imprime os processos que mais consomem cpu
    def __str__(self):
        print 'Processos - Maior Consumo Cpu'
        for p in self.proc:
            print p
        return ''


# Classe que represente as informacoes de Disco
class Disco:
    def __init__(self, gb, porcento):
        self.gb = gb
        self.porcento = porcento

    # imprime os dados de disco
    def __str__(self):
        print 'Disco : '
        print '      : ' + str(self.gb) + ' Gb'
        print '      : ' + str(self.porcento) + ' %'
        return ''


# funcao que imprime um determinado recurso a partir de recursos ja coletados
def coleta_recurso(tipo_recurso,quantidade):
    global recursos
    tipo_recurso = int(tipo_recurso)
    quantidade = int(quantidade)
    # copia da estrutura pois a original deve continuar coletando recursos
    rec = copy.copy(recursos)

    if quantidade > len(rec):
        quantidade = len(rec)

    # dependendo do tipo pedido e impresso a hora que foi coletado o recurso
    # e as informacoes do recurso
    if tipo_recurso is COLETA_CPU:
        for r in xrange(quantidade):
            print r.formata_tempo()
            print r.cpu
    elif tipo_recurso is COLETA_MEMORIA:
        for r in xrange(quantidade):
            print r.formata_tempo()
            print r.memoria
    elif tipo_recurso is COLETA_SWAP:
        for r in xrange(quantidade):
            print r.formata_tempo()
            print r.swap
    elif tipo_recurso is COLETA_REDE:
        for r in xrange(quantidade):
            print r.formata_tempo()
            print r.rede
    elif tipo_recurso is COLETA_NUM_PROCESSOS_ATIVOS:
        for r in xrange(quantidade):
            print r.formata_tempo()
            print r.num_processos_ativos
    elif tipo_recurso is COLETA_MAX_PROC_MEM:
        for r in xrange(quantidade):
            print r.formata_tempo()
            print r.cinco_processos_mem
    elif tipo_recurso is COLETA_MAX_PROC_CPU:
        for r in xrange(quantidade):
            print r.formata_tempo()
            print r.cinco_processos_cpu
    elif tipo_recurso is COLETA_DISCO:
        for r in xrange(quantidade):
            print r.formata_tempo()
            print r.disco


# Funcao que salva os recursos de tempos em tempos
def salva_recursos():
    global recursos

    while True:
        # cria um objeto do tipo Recursos
        r = Recursos()
        # salva informacao de cpu
        r.registra_cpu(Cpu(psutil.cpu_percent(interval=0)))
        # salva informacao de memoria virtual
        mem = psutil.virtual_memory()
        r.registra_memoria(
            Memoria(str(int(mem.used / 1024.0 / 1024.0)) + '/' + str(int(mem.total / 1024.0 / 1024.0)), mem.percent))
        # salva informacao de memoria swap
        mem = psutil.swap_memory()
        r.registra_swap(
            MemoriaSwap(str("%.1f" % (mem.used / 1024.0 / 1024.0)) + '/' + str(int(mem.total / 1024.0 / 1024.0)),
                        mem.percent))
        # salva informacao de rede
        rede = psutil.net_io_counters(pernic=True)
        rec_rede = Rede()
        # registra cada interface e seus dados de trafego
        for interface in rede:
            rec_rede.insere_interface(interface, rede[interface].packets_sent, rede[interface].packets_recv)
        r.registra_rede(rec_rede)
        # pega os processos do sistema
        processos = psutil.pids()
        # salva numero de processos ativos
        r.registra_num_proc_ativos(len(processos))

        proc_list = {}

        # percorre a lista de todos os processos do sistema e salva em uma lista as informacoes do processo, seu consumo de memoria e cpu
        for pid in processos:

            try:
                # obtem processo
                proc = psutil.Process(pid)
                if proc is not None:
                    m = proc.memory_percent()
                    proc.cpu_percent()
                    # salva processo na lista
                    proc_list[pid] = [proc, m, proc.cpu_percent(interval=0.0)]
            except:
                # error tentando pegar informacao de processo'
                pass

        # ordena a lista de processos pelo consumo de memoria e guarda na lista top_five_mem_proc
        top_five_mem_proc = sorted(proc_list, key=lambda tup: proc_list[tup][1], reverse=True)
        # ordena a lista de processos pelo consumo de cpu e guarda na lista top_five_cpu_proc
        top_five_cpu_proc = sorted(proc_list, key=lambda tup: proc_list[tup][2], reverse=True)

        # registra os 5 cinco processos que mais consomem memoria
        pmm = ProcessosMaxMemoria()
        for i in range(5):
            pmm.adiciona_processo(
                Processo(proc_list[top_five_mem_proc[i]][0].pid, proc_list[top_five_mem_proc[i]][0].name(),
                         proc_list[top_five_mem_proc[i]][0].username(),
                         proc_list[top_five_mem_proc[i]][0].create_time(), proc_list[top_five_mem_proc[i]][1],
                         proc_list[top_five_mem_proc[i]][2]))

        r.registra_cinco_proc_mem(pmm)

        # registra os 5 cinco processos que mais consomem cpu
        pmc = ProcessosMaxCpu()

        for i in range(5):
            pmc.adiciona_processo(
                Processo(proc_list[top_five_cpu_proc[i]][0].pid, proc_list[top_five_cpu_proc[i]][0].name(),
                         proc_list[top_five_cpu_proc[i]][0].username(),
                         proc_list[top_five_cpu_proc[i]][0].create_time(), proc_list[top_five_cpu_proc[i]][1],
                         proc_list[top_five_cpu_proc[i]][2]))

        r.registra_cinco_proc_cpu(pmc)

        # salva informacao de disco
        uso_disco = psutil.disk_usage('/')
        tam_total = uso_disco.total / 1024.0 / 1024.0 / 1024.0
        tam_usado = uso_disco.used / 1024.0 / 1024.0 / 1024.0
        r.registra_disco(Disco(str(tam_usado) + '/' + str(tam_total), str(uso_disco.percent)))

        # Registra os recursos coletados na estrutura que guarda todos os registros
        recursos.append(r)

        # espera para coletar
        time.sleep(INTERVALO_TEMPO)


# tamanho da janela deslizante, deve ser 1000, mas pra teste 5
TAMANHO_JANELA_DESLIZANTE = 5
# tempo de espera 100 ms
INTERVALO_TEMPO = 0.01

# estrutura para guardar os recursos coletados, essa estrutura funciona exatamente como uma janela deslizante
recursos = deque("", TAMANHO_JANELA_DESLIZANTE)

# cria nova thread para rodar a funcao que salva os recursos
recursos_thread = Thread(target=salva_recursos)
recursos_thread.start()

# Para testar - funcao que sempre pede um valor correspondente a um recurso para imprimir na tela
while True:
    # le do teclado identificador do recurso
    opcao_recurso = raw_input("Digite o recurso\n")
    quant_recurso = raw_input("Quantidade de medicoes do recurso\n")
    # chama funcao para imprimir informacoes coletadas do recurso pedido
    coleta_recurso(opcao_recurso,quant_recurso)
