import psutil

PORT = 50999

class Medida:


	def __init__(self, cpu, memoria, swap, rede, num_processos_ativos, cinco_processos_mem, cinco_processos_cpu, disco):

		self.cpu = cpu
		self.memoria = memoria
		self.swap = swap
		self.rede = rede
		self.num_processos_ativos = num_processos_ativos
		self.cinco_processos_mem = cinco_processos_mem
		self.cinco_processos_cpu = cinco_processos_cpu
		self.disco = disco



#Consumo de CPU (%)
uso_cpu = psutil.cpu_percent(interval=1)
print 'Uso de CPU (%) ' + str(uso_cpu)

#Consumo de Memoria (MB e %)
mem = psutil.virtual_memory()
uso_memoria = {}
uso_memoria['%'] = mem.percent
uso_memoria['MB'] = str(mem.used / 1024.0 / 1024.0) + '/' + str(mem.total / 1024.0 / 1024.0)
print 'Uso de Memoria (MB e %)' + str(uso_memoria)

#Consumo de SWAP (MB e %)
swap = psutil.swap_memory()
uso_swap = {}
uso_swap['%'] = swap.percent
uso_swap['MB'] = str(swap.used / 1024.0 / 1024.0) + '/' + str(swap.total / 1024.0 / 1024.0)
print 'Uso de SWAP (MB e %)' + str(uso_swap)

#Trafego de Dados - Interfaces de Rede
rede = psutil.net_io_counters(pernic=True)
print rede
uso_rede = {}

#Numero de processos ativos
processos = psutil.pids()
num_processos_ativos = len(processos)
print 'Numero de Processos Ativos ' + str(num_processos_ativos)

proc_list = {}

def getKey(item):
	global proc_list
	return proc_list[item][1]

for pid in processos:
	proc = psutil.Process(pid)
	if proc is not None:
		proc_list[pid] = [proc, proc.memory_percent()]

top_five_mem_proc = sorted(proc_list, key=getKey,reverse=True)

print 'Processos com maior consumo de memoria'
for i in range(5):
	print '## '  + str(i+1) + '## '
	p  = proc_list[top_five_mem_proc[i]][0]
	print 'PID ' + str(p.pid)
	print 'Nome ' + str(p.name())
	print 'Dono ' + str(p.username())
	print 'Tempo ' + str(p.create_time())
	print 'Consumo de memoria ' + str(p.memory_percent()) + ' %'
	print '\n'

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
uso_disco = psutil.disk_usage('/')
tam_total =  uso_disco.total / 1024.0 / 1024.0 / 1024.0
tam_usado =  uso_disco.used / 1024.0 / 1024.0 / 1024.0
print 'Uso do Disco ' + str(tam_usado) + '/' + str(tam_total) + 'GB - ' + str(uso_disco.percent) + '%'

