import socket
from threading import Thread, BoundedSemaphore
import sys
import linecache
from datetime import datetime
import wx


# Classe que representa a janela para inserir os dados do servidor
class JanelaDadoColetor(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaDadoColetor, self).__init__(parent, -1, 'Dados do Coletor', style=style)

        # Configuracao de elementos de tela
        self.ip_texto = wx.StaticText(self, -1, "Digite o ip")
        self.ip_entrada = wx.TextCtrl(self, value="")
        self.ip_entrada.SetInitialSize((200, 20))
        self.porta_texto = wx.StaticText(self, -1, "Digite a porta")
        self.porta_entrada = wx.TextCtrl(self, value="")
        self.porta_entrada.SetInitialSize((200, 20))
        botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ip_texto, 0, wx.ALL, 5)
        sizer.Add(self.ip_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.porta_texto, 0, wx.ALL, 5)
        sizer.Add(self.porta_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    # funcao para pegar os dados inseridos na janela
    def pegar_dados_coletor(self):
        return self.ip_entrada.GetValue() + "," + self.porta_entrada.GetValue()


# Classe que representa a janela para inserir os dados para entrar em um leilao
class JanelaCadastrarMaquina(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaCadastrarMaquina, self).__init__(parent, -1, 'Cadastrar uma maquina', style=style)
        # Configuracao de elementos de tela
        self.cadastro_texto = wx.StaticText(self, -1, "Digite o IP da maquina monitorada")
        self.ip_maquina = wx.TextCtrl(self, value="")
        self.ip_maquina.SetInitialSize((200, 20))
        self.botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cadastro_texto, 0, wx.ALL, 5)
        sizer.Add(self.ip_maquina, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    # funcao para pegar os dados inseridos na janela
    def pegar_ip_maquina(self):
        return self.ip_maquina.GetValue()

class JanelaColetaRecurso(wx.Dialog):
    pass

# Classe que representa a tela principal
class TelaLeilao(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Monitoramento de Sistema UFF", size=(1000, 280))

        # Configuracao de elementos de tela

        # Configuracoes de textos, botoes e os eventos de clique dos botoes
        self.bem_vindo = wx.StaticText(self, label="Bem vindo ao Monitoramento de Sistema UFF", pos=(20, 10))
        self.botao_cadastrar_maquina = wx.Button(self, label="Cadastrar Maquina", pos=(20, 60))
        self.Bind(wx.EVT_BUTTON, botao_cadastrar_maquina, self.botao_cadastrar_maquina)

        self.botao_listar_maquinas = wx.Button(self, label="Listar Maquinas Cadastradas", pos=(20, 90))
        self.Bind(wx.EVT_BUTTON, botao_listar_maquinas, self.botao_listar_maquinas)

        self.botao_coletar_recurso = wx.Button(self, label="Coletar Recurso", pos=(20, 120))
        self.Bind(wx.EVT_BUTTON, botao_coletar_recurso, self.botao_coletar_recurso)

        self.botao_sair = wx.Button(self, label="Sair", pos=(20, 150))
        self.Bind(wx.EVT_BUTTON, botao_sair, self.botao_sair)


# funcao de evento de clique do botao para cadastrar usuario
def botao_cadastrar_maquina(evento):
    global s_operacao_atual, operacao_atual

    # criacao da janela de cadastro de usuario
    janela = JanelaCadastrarMaquina(None)
    janela.Center()
    dados = None
    if janela.ShowModal() == wx.ID_OK:
        # apos clicar em OK da janela, pega as informacoes inseridas na janela
        dados = janela.pegar_ip_maquina()
    janela.Destroy()

    if dados is not None:
        envia_mensagem_coletor(str('cadastro,' + dados))


# funcao de evento de clique do botao para cadastrar usuario
def botao_listar_maquinas(evento):
    # criacao da janela de cadastro de usuario
    envia_mensagem_coletor('lista')

# funcao de evento de clique do botao para cadastrar usuario
def botao_coletar_recurso(evento):
    # criacao da janela de cadastro de usuario
    janela = JanelaColetaRecurso(None)
    janela.Center()
    dados = None
    if janela.ShowModal() == wx.ID_OK:
        # apos clicar em OK da janela, pega as informacoes inseridas na janela
        dados = janela.pegar_ip_maquina()
    janela.Destroy()

    if dados is not None:
        dados = dados.split(',')
        envia_mensagem_coletor(str('recurso,' + dados[0] + ',' + dados[1] + ',' + dados[2]))

def botao_sair(evento):
    pass

# Soluca da internet para ver todas as informacoes sobre o erro dentro do except:
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


# Funcao que envia mensagem para o servidor
def envia_mensagem_coletor(mensagem):
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
    if conecta_servidor():
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


# Thread que escuta as mensagens vindas do servidor
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


try:

    #cria interface grafica
    app = wx.App(False)

    #cria janela com dados do servidor
    janela = JanelaDadoColetor(None)
    janela.Center()
    if janela.ShowModal() == wx.ID_OK:
        dados_servidor = janela.pegar_dados_servidor().split(',')
        host_ip = dados_servidor[0]
        porta = int(dados_servidor[1])
        estabelece_conexao_servidor(host_ip, porta)
        #conecta servidor
        s_servidor_contectado.acquire()
        if servidor_conectado:
            #executa thread para escutar as mensagens
            t = Thread(target=escuta_servidor)
            t.setDaemon(True)
            t.start()
            #criacao da tela principal
            tela = TelaLeilao()
            tela.Show()
        else:
            #cria janela de aviso para mostrar que nao foi possivel conectar
            janela_aviso = JanelaAviso(None, 'Nao foi possivel conectar ao servidor')
            janela_aviso.Center()
            janela_aviso.ShowModal()
            janela_aviso.Destroy()
        s_servidor_contectado.release()
    janela.Destroy()
    app.MainLoop()

# Por final, desconecta serviddor
finally:
    desconecta_servidor()

