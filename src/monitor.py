import psutil
from collections import deque
import time
from threading import Thread
import copy

PORT = 50999

COLETA_CPU = 0
COLETA_MEMORIA = 1
COLETA_SWAP = 2
COLETA_REDE = 3
COLETA_NUM_PROCESSOS_ATIVOS = 4
COLETA_MAX_PROC_MEM = 5
COLETA_MAX_PROC_CPU = 6
COLETA_DISCO = 7

class Recursos:


#	def __init__(self, cpu, memoria, swap, rede, num_processos_ativos, cinco_processos_mem, cinco_processos_cpu, disco):
#
#		self.cpu = cpu
#		self.memoria = memoria
#		self.swap = swap
#		self.rede = rede
#		self.num_processos_ativos = num_processos_ativos
#		self.cinco_processos_mem = cinco_processos_mem
#		self.cinco_processos_cpu = cinco_processos_cpu
#		self.disco = disco

	def __init_(self):
		self.tempo = time.time()
		self.cpu = None
		self.memoria = None
		self.swap = None
		self.rede = None
		self.num_processos_ativos = None
		self.cinco_processos_mem = None
		self.cinco_processos_cpu = None
		self.disco = None


	def __str__(self):
		print self.tempo
		print self.cpu
		print self.memoria
		print self.swap
		print self.rede
		print 'Numero de Processos ativos: ' + str(self.num_processos_ativos)
		print self.cinco_processos_mem
		print self.cinco_processos_cpu
		print self.disco
		return ''


	def registra_cpu(self, cpu):
		self.cpu = cpu

	def registra_memoria(self, memoria):
		self.memoria = memoria

	def registra_swap(self, swap):
		self.swap = swap

	def registra_rede(self, rede):
		self.rede = rede

	def registra_num_proc_ativos(self, num_proc_ativos):
		self.num_processos_ativos = num_proc_ativos

	def registra_cinco_proc_mem(self, proc_mem):
		self.cinco_processos_mem = proc_mem

	def registra_cinco_proc_cpu(self, proc_cpu):
		self.cinco_processos_cpu = proc_cpu

	def registra_disco(self, disco):
		self.disco = disco

class Memoria:

	def __init__(self, mb, porcento):
		self.mb = mb
		self.porcento = porcento

	def __str__(self):
		print 'Memoria Virtual : '
		print '                : ' + str(self.mb) + ' MB'
		print '                : ' + str(self.porcento) + ' %'
		return ''

class Memoria_Swap:

	def __init__(self, mb, porcento):
		self.mb = mb
		self.porcento = porcento

	def __str__(self):
		print 'Memoria Swap : '
		print '             : ' + str(self.mb) + ' MB'
		print '             : ' + str(self.porcento) + ' %'
		return ''

class Cpu:

	def __init__(self, porcento):
		self.porcento = porcento

	def __str__(self):
		print 'CPU : '
		print '    : ' + str(self.porcento) + ' %'
		return ''

class Rede:

	def __init__(self):
		self.rede = {}

	def insere_interface(self, interface, pacotes_enviados, pacotes_recebidos):
		self.rede[interface] = [pacotes_enviados, pacotes_recebidos]

	def __str__(self):
		print 'Rede : '
		for interface in self.rede:
			print '        Interface : ' + str(interface)
			print '                  : Pacotes Enviados : ' + str(self.rede[interface][0])
			print '                  : Pacotes Recebidos: ' + str(self.rede[interface][1])
		return ''


class Processo:

	def __init__(self,pid,nome,dono,tempo,mem,cpu):
		self.pid = pid
		self.nome = nome
		self.dono = dono
		self.tempo = tempo
		self.mem = mem
		self.cpu = cpu

	def __str__(self):
		print '      PID ' + str(self.pid)
		print '      Nome ' + str(self.nome)
		print '      Dono ' + str(self.dono)
		print '      Tempo ' + str(self.tempo)
		print '      Consumo de memoria ' + str(self.mem) + '%'
		print '      Consumo de cpu ' + str(self.cpu) + '%'
		return ''


class Processos_Max_Memoria:

	def __init__(self):
		self.proc = {}

	def adiciona_processo(self, processo):
		self.proc[processo] = processo

	def __str__(self):

		print 'Processos - Maior Consumo Memoria'
		for p in self.proc:
			print p
		return ''

class Processos_Max_Cpu:

	def __init__(self):
		self.proc = {}

	def adiciona_processo(self, processo):
		self.proc[processo] = processo

	def __str__(self):

		print 'Processos - Maior Consumo Cpu'
		for p in self.proc:
			print p
		return ''

class Disco:

	def __init__(self, gb,porcento):
		self.gb = gb
		self.porcento = porcento

	def __str__(self):
		print 'Disco : '
		print '      : ' + str(self.gb) + ' Gb'
		print '      : ' + str(self.porcento) + ' %'
		return ''

#Consumo de CPU (%)
#uso_cpu = psutil.cpu_percent(interval=1)
#print 'Uso de CPU (%) ' + str(uso_cpu)

#Consumo de Memoria (MB e %)
#mem = psutil.virtual_memory()
#uso_memoria = {}
#uso_memoria['%'] = mem.percent
#uso_memoria['MB'] = str(mem.used / 1024.0 / 1024.0) + '/' + str(mem.total / 1024.0 / 1024.0)
#print 'Uso de Memoria (MB e %)' + str(uso_memoria)

#Consumo de SWAP (MB e %)
#swap = psutil.swap_memory()
#uso_swap = {}
#uso_swap['%'] = swap.percent
#uso_swap['MB'] = str(swap.used / 1024.0 / 1024.0) + '/' + str(swap.total / 1024.0 / 1024.0)
#print 'Uso de SWAP (MB e %)' + str(uso_swap)

#Trafego de Dados - Interfaces de Rede
#rede = psutil.net_io_counters(pernic=True)
#uso_rede = {}
#for interface in rede:
#	uso_rede[interface] = [ rede[interface].packets_sent , rede[interface].packets_recv ]

#for ur in uso_rede:#
#	print 'Interface ' + ur + ':'
#	print '        Pacotes Enviados ' + str(uso_rede[ur][0])
#	print '        Pacotes Recebidos ' + str(uso_rede[ur][1])

#Numero de processos ativos
#processos = psutil.pids()
#num_processos_ativos = len(processos)
#print 'Numero de Processos Ativos ' + str(num_processos_ativos)

#proc_list = {}

#def ordena_pela_memoria(item):
#	global proc_list
#	return proc_list[item][1]
#
#def ordena_pela_cpu(item):
#	global proc_list
#	return proc_list[item][2]
#counter = 1
#for pid in processos:
#	#print "Calculating Processes information ", str(counter) + '/' + str(num_processos_ativos) + "\r",
#	try:
#		proc = psutil.Process(pid)
#		if proc is not None:
#			proc.cpu_percent()
#			proc_list[pid] = [proc, proc.memory_percent(), proc.cpu_percent(interval=0.5)]
#			print str(proc.name())
#	except:
#		print 'error when getting process information'
#	counter = counter + 1
#
#top_five_mem_proc = sorted(proc_list, key=ordena_pela_memoria,reverse=True)
#top_five_cpu_proc = sorted(proc_list, key=ordena_pela_cpu, reverse=True)
#
#def imprime_top_five(procs, label):
#
#	print 'Processos com maior consumo de ' + label
#	for i in range(5):
#		print '## '  + str(i+1) + ' ##'
#		p  = proc_list[top_five_mem_proc[i]][0]
#		print 'PID ' + str(p.pid)
#		print 'Nome ' + str(p.name())
#		print 'Dono ' + str(p.username())
#		print 'Tempo ' + str(p.create_time())
#		if label is 'mem':
#			print 'Consumo de memoria ' + str(proc_list[top_five_mem_proc[i]][1]) + '%'
#		else :
#			print 'Consumo de cpu ' + str(proc_list[top_five_cpu_proc[i]][2]) + '%'
#		print '\n'
#
#imprime_top_five(top_five_mem_proc, 'mem')
#imprime_top_five(top_five_cpu_proc,'cpu')

#for tpid in top_five_mem_proc:
#	print 'PID ' + str(proc_list[tpid][0].name

#for pid in processos:
#	proc = psutil.Process(pid)
#	if proc is not None:
#		print 'PID ' + str(proc.pid)
#		print 'Nome ' + str(proc.name())
#		print 'User ' + str(proc.username())
#		print 'Time ' + str(proc.create_time())
#		print 'CPU % ' + str(proc.memory_percent())
#		print 'Mem % ' + str(proc.cpu_percent())
#	print '\n\n'

#uso de Discos
#uso_disco = psutil.disk_usage('/')
#tam_total =  uso_disco.total / 1024.0 / 1024.0 / 1024.0
#tam_usado =  uso_disco.used / 1024.0 / 1024.0 / 1024.0
#print 'Uso do Disco ' + str(tam_usado) + '/' + str(tam_total) + 'GB - ' + str(uso_disco.percent) + '%'

#def ordena_pela_memoria(item):
#	global proc_list
#	return proc_list[item][1]

#def ordena_pela_cpu(item):
#	global proc_list
#	return proc_list[item][2]


def coleta_recurso(tipo_recurso):

	global recursos
	tipo_recurso = int(tipo_recurso)
	rec = copy.copy(recursos)

	if tipo_recurso is COLETA_CPU:
		for r in rec:
			#print r.tempo
			print r.cpu
	elif tipo_recurso is COLETA_MEMORIA:
		for r in rec:
			print r.memoria
	elif tipo_recurso is COLETA_SWAP:
		for r in rec:
			print r.swap
	elif tipo_recurso is COLETA_REDE:
		for r in rec:
			print r.rede
	elif tipo_recurso is COLETA_NUM_PROCESSOS_ATIVOS:
		for r in rec:
			print r.num_processos_ativos
	elif tipo_recurso is COLETA_MAX_PROC_MEM:
		for r in rec:
			print r.cinco_processos_mem
	elif tipo_recurso is COLETA_MAX_PROC_CPU:
		for r in rec:
			print r.cinco_processos_cpu
	elif tipo_recurso is COLETA_DISCO:
		for r in rec:
			print r.disco

def salva_recursos():

	global recursos
	c = 0
	#while c < 2:
	while True:
#		print 'it ' + str(c)
		r = Recursos()
		r.registra_cpu(Cpu(psutil.cpu_percent(interval=0)))
		mem = psutil.virtual_memory()
		r.registra_memoria(Memoria(str(mem.used / 1024.0 / 1024.0) + '/' + str(mem.total / 1024.0 / 1024.0),mem.percent))
		mem = psutil.swap_memory()
		r.registra_swap(Memoria_Swap(str(mem.used / 1024.0 / 1024.0) + '/' + str(mem.total / 1024.0 / 1024.0),mem.percent))
		rede = psutil.net_io_counters(pernic=True)
		rec_rede = Rede()
		for interface in rede:
			rec_rede.insere_interface(interface, rede[interface].packets_sent, rede[interface].packets_recv)
		r.registra_rede(rec_rede)
		processos = psutil.pids()
		r.registra_num_proc_ativos(len(processos))

		proc_list = {}

		for pid in processos:

			try:
				proc = psutil.Process(pid)
				if proc is not None:
					proc.cpu_percent()
					proc_list[pid] = [proc, proc.memory_percent(), proc.cpu_percent(interval=0.0)]
#					print str(proc.name())
			except:
				print 'error when getting process information'

		top_five_mem_proc = sorted(proc_list, key=lambda tup: proc_list[tup][0],reverse=True)
		top_five_cpu_proc = sorted(proc_list, key=lambda tup: proc_list[tup][1], reverse=True)

		pmm = Processos_Max_Memoria()

		for i in range(5):
			pmm.adiciona_processo(Processo(proc_list[top_five_mem_proc[i]][0].pid,proc_list[top_five_mem_proc[i]][0].name(),proc_list[top_five_mem_proc[i]][0].username(),proc_list[top_five_mem_proc[i]][0].create_time(),proc_list[top_five_mem_proc[i]][1],proc_list[top_five_mem_proc[i]][2]))

		r.registra_cinco_proc_mem(pmm)
		pmc = Processos_Max_Cpu()

		for i in range(5):
			pmc.adiciona_processo(Processo(proc_list[top_five_mem_proc[i]][0].pid,proc_list[top_five_mem_proc[i]][0].name(),proc_list[top_five_mem_proc[i]][0].username(),proc_list[top_five_mem_proc[i]][0].create_time(),proc_list[top_five_mem_proc[i]][1],proc_list[top_five_mem_proc[i]][2]))

		r.registra_cinco_proc_cpu(pmc)

		uso_disco = psutil.disk_usage('/')
		tam_total =  uso_disco.total / 1024.0 / 1024.0 / 1024.0
		tam_usado =  uso_disco.used / 1024.0 / 1024.0 / 1024.0
		r.registra_disco(Disco(str(tam_usado) + '/' + str(tam_total),str(uso_disco.percent)))

		recursos.append(r)

		time.sleep(INTERVALO_TEMPO)
		c = c+1

	#print 'Quantidade de recursos coletados ' + str(len(recursos))
	#for r in recursos:
	#	print r

TAMANHO_JANELA_DESLIZANTE = 5
INTERVALO_TEMPO = 0.01

recursos = deque("",TAMANHO_JANELA_DESLIZANTE)

#medidas_cpu = deque("",TAMANHO_JANELA_DESLIZAN#$TE)
#medidas_memoria = deque("",TAMANHO_JANELA_DESLIZANTE)
#medidas_memoria_swap = deque("",TAMANHO_JANELA_DESLIZANTE)
#medidas_rede = deque("",TAMANHO_JANELA_DESLIZANTE)
#medidas_processos_max_memoria = deque("",TAMANHO_JANELA_DESLIZANTE)
#medidas_processos_max_cpu = deque("",TAMANHO_JANELA_DESLIZANTE)
#medidas_num_processos = deque("",TAMANHO_JANELA_DESLIZANTE)
#medidas_disco = deque("",TAMANHO_JANELA_DESLIZANTE)


recursos_thread = Thread(target=salva_recursos)
recursos_thread.start()

while True:
	option = raw_input("Digite o recurso\n")
	coleta_recurso(option)
