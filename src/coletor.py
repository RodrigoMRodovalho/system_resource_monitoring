COLETOR_PORTA = 50033
ARQUIVO_CADASTRO_MAQUINAS = "maquinas.txt"

# funcao que cadastra uma maquina
def cadastra_maquina(ip):
	#salva o ip da maquina em arquivo
	pass

# funcao que retorna a lista de maquinas cadastradas
def lista_maquinas_cadastradas():
	#le maquinas do arquivo
	pass
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

# funcao que recebe requisicao
def recebe_requisicao():
	pass

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











