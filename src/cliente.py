import socket
from threading import Thread, BoundedSemaphore
import sys
import linecache
from datetime import datetime
import wx
import wx.grid as gridlib


# Classe que representa a janela de aviso
class JanelaAviso(wx.Dialog):
    def __init__(self, parent, texto):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaAviso, self).__init__(parent, -1, 'Aviso', style=style)
        # Configuracao de elementos de tela
        self.aviso_texto = wx.StaticText(self, -1, texto)
        self.botoes = self.CreateButtonSizer(wx.OK)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.aviso_texto, 0, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)


# Classe que representa a janela para inserir os dados do coletor
class JanelaDadoColetor(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaDadoColetor, self).__init__(parent, -1, 'Dados do Coletor', style=style)

        # Configuracao de elementos de tela
        self.ip_texto = wx.StaticText(self, -1, "Digite o ip")
        self.ip_entrada = wx.TextCtrl(self, value="127.0.0.1")
        self.ip_entrada.SetInitialSize((200, 20))
        self.porta_texto = wx.StaticText(self, -1, "Digite a porta")
        self.porta_entrada = wx.TextCtrl(self, value="50053")
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
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaColetaRecurso, self).__init__(parent, -1, 'Coleta de Recurso Monitorado',
                                                  style=style)
        self.ip_maquina_texto = wx.StaticText(self, -1, "Digite o IP da maquina monitorada")
        self.ip_maquina = wx.TextCtrl(self, value="127.0.0.1")
        self.ip_maquina.SetInitialSize((200, 20))

        recursos = [
            'Consumo de CPU',
            'Consumo de memoria',
            'Uso da swap',
            'Taxa de saida e de entrada de pacotes nas interfaces de Rede',
            'Numero de processos ativos',
            '5 Processos com maior consumo de Memoria',
            '5 Processos com maior consumo de CPU',
            'Uso de Disco'
        ]

        self.recurso_texto = wx.StaticText(self, -1, "Escolha o recurso")
        self.escolhe_recurso = wx.Choice(self, choices=recursos)

        self.quantidade_texto = wx.StaticText(self, -1, "Digite a quantidade de medicoes")
        self.quantidade = wx.TextCtrl(self, value="")
        self.quantidade.SetInitialSize((200, 20))

        botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ip_maquina_texto, 0, wx.ALL, 5)
        sizer.Add(self.ip_maquina, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.recurso_texto, 0, wx.ALL, 5)
        sizer.Add(self.escolhe_recurso, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.quantidade_texto, 0, wx.ALL, 5)
        sizer.Add(self.quantidade, wx.EXPAND, wx.ALL, 5)
        sizer.Add(botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    def pega_recurso_escolhido(self):
        return str(self.ip_maquina.GetValue()) + ',' + \
               str(self.escolhe_recurso.GetSelection()) + ',' + \
               str(self.quantidade.GetValue())


class JanelaListaMaquinasCadastradas(wx.Dialog):
    def __init__(self, parent, listagem_maquinas):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaListaMaquinasCadastradas, self).__init__(parent, -1, 'Listagem de maquinas cadastradas',
                                                             style=style)

        listagem_maquinas = listagem_maquinas.replace('lista,', '').split(',')
        tabela = gridlib.Grid(self,size=(320,300))
        tabela.CreateGrid(len(listagem_maquinas), 1)
        tabela.SetColLabelValue(0, "IP")
        tabela.SetColSize(0, 130)

        linha = 0
        for maquina_ip in listagem_maquinas:
            tabela.SetCellValue(linha, 0, maquina_ip)
            tabela.SetReadOnly(linha, 0, True)
            linha = linha + 1

        botoes = self.CreateButtonSizer(wx.OK)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tabela, 0, wx.CENTER | wx.ALL, 5)
        sizer.Add(botoes, 0, wx.CENTER | wx.ALL, 5)
        self.SetSizerAndFit(sizer)


class JanelaRecursosColetados(wx.Dialog):
    def __init__(self, parent, recurso_coletado):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaRecursosColetados, self).__init__(parent, -1, 'Recurso coletado de IP', style=style)

        # todo implement body

        botoes = self.CreateButtonSizer(wx.OK)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)


# Classe que representa a tela principal
class TelaSistema(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Monitoramento de Sistema UFF", size=(400, 280))

        # Configuracao de elementos de tela

        # Configuracoes de textos, botoes e os eventos de clique dos botoes
        self.bem_vindo = wx.StaticText(self, label="Bem vindo ao Sistema de Monitoramento de maquinas - UFF",
                                       pos=(20, 10))
        self.botao_cadastrar_maquina = wx.Button(self, label="Cadastrar Maquina", pos=(20, 60))
        self.Bind(wx.EVT_BUTTON, botao_cadastrar_maquina, self.botao_cadastrar_maquina)

        self.botao_listar_maquinas = wx.Button(self, label="Listar Maquinas Cadastradas", pos=(20, 90))
        self.Bind(wx.EVT_BUTTON, botao_listar_maquinas, self.botao_listar_maquinas)

        self.botao_coletar_recurso = wx.Button(self, label="Coletar Recurso", pos=(20, 120))
        self.Bind(wx.EVT_BUTTON, botao_coletar_recurso, self.botao_coletar_recurso)

        self.botao_sair = wx.Button(self, label="Sair", pos=(20, 150))
        self.Bind(wx.EVT_BUTTON, botao_sair, self.botao_sair)

    # funcao que cria uma janela de aviso
    def mostra_janela_aviso(self, aviso):
        j_aviso = JanelaAviso(None, aviso)
        j_aviso.Center()
        j_aviso.ShowModal()
        j_aviso.Destroy()

    def mostra_erro(self):
        self.mostra_janela_aviso('Ocorreu um erro')

    def mostra_cadastro(self, msg):

        if 'NOk' in msg:
            self.mostra_janela_aviso('Nao foi possivel cadastrar maquina')
        else:
            self.mostra_janela_aviso('Maquina cadastrada com sucesso')

    def mostra_lista_maquinas(self, msg):

        if msg == 'lista,':
            self.mostra_janela_aviso('Nenhuma maquina cadastrada')
        else:
            j_lista_maquinas = JanelaListaMaquinasCadastradas(None, msg)
            j_lista_maquinas.Center()
            j_lista_maquinas.ShowModal()
            j_lista_maquinas.Destroy()

    def mostra_recurso(self, msg):
        j_lista_maquinas = JanelaRecursosColetados(None, msg)
        j_lista_maquinas.Center()
        j_lista_maquinas.ShowModal()
        j_lista_maquinas.Destroy()


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
        envia_mensagem_coletor(str('cadastra,' + dados))


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
        dados = janela.pega_recurso_escolhido()
    janela.Destroy()

    if dados is not None:
        envia_mensagem_coletor(str('recurso,' + dados))


def botao_sair(evento):
    global tela
    tela.Destroy()


# Soluca da internet para ver todas as informacoes sobre o erro dentro do except:
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


# Funcao que envia mensagem para o coletor
def envia_mensagem_coletor(mensagem):
    print >> sys.stderr, 'enviando ', mensagem, '  as ', datetime.now().time()
    coletor_sock.sendall(mensagem)


# Imprime as mensagens recebidas
def log_mensagem_recebida(mensagem):
    print >> sys.stderr, 'recebido ', mensagem, '  at ', datetime.now().time()


# Funcao que guarda nas variaveis o IP e Porta do coletor
def configura_coletor(host, port):
    global host_ip, porta
    host_ip = host
    porta = port


# Funcao que conecta socket do coletor
def conecta_coletor():
    global coletor_sock
    try:
        # Cria socket para conexao
        coletor_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configura endereco - IP e Porta
        endereco_coletor = (host_ip, porta)
        print >> sys.stderr, 'Conectando em %s port %s' % endereco_coletor
        coletor_sock.connect(endereco_coletor)
        print >> sys.stderr, 'Conectado'
        return True
    except:
        return False


# Funcao que desconecta socket do coletor
def desconecta_coletor():
    coletor_sock.close()


# Funcao que realiza comunicacao com coletor
def estabelece_conexao_coletor(host_ip, porta):
    global s_coletor_contectado, coletor_conectado, mensagem_erro

    # Configura IP e Porta do coletor
    configura_coletor(host_ip, porta)
    # Verifica se conecta com o coletor
    if conecta_coletor():
        # mensagem_erro = None
        # Libera a variavel que controla se conectou o coletor ou se deu erro
        s_coletor_contectado.acquire()
        coletor_conectado = True
        s_coletor_contectado.release()
    else:
        # mensagem_erro = 'Nao foi possivel conectar ao coletor'
        # Libera a variavel que controla se conectou o coletor ou se deu erro
        s_coletor_contectado.acquire()
        coletor_conectado = False
        s_coletor_contectado.release()


# Thread que escuta as mensagens vindas do coletor
def escuta_coletor():
    while True:
        msg = coletor_sock.recv(4096)
        log_mensagem_recebida(msg)

        if msg == 'NOk':
            wx.CallAfter(tela.mostra_erro, '')
        elif 'cadastra' in msg:
            wx.CallAfter(tela.mostra_cadastro, str(msg))
        elif 'lista' in msg:
            wx.CallAfter(tela.mostra_lista_maquinas, str(msg))
        elif 'recurso' in msg:
            wx.CallAfter(tela.mostra_recurso, str(msg))
        else:
            print 'mensagem desconhecida'


host_ip = '127.0.0.1'
porta = 50053
# Declaracao do socket de conexao com coletor
coletor_sock = None
coletor_conectado = False
s_coletor_contectado = BoundedSemaphore()

tela = None

try:

    # cria interface grafica
    app = wx.App(False)

    # cria janela com dados do coletor
    janela = JanelaDadoColetor(None)
    janela.Center()
    if janela.ShowModal() == wx.ID_OK:
        dados_coletor = janela.pegar_dados_coletor().split(',')
        host_ip = dados_coletor[0]
        porta = int(dados_coletor[1])
        estabelece_conexao_coletor(host_ip, porta)
        # conecta coletor
        s_coletor_contectado.acquire()
        if coletor_conectado:
            # executa thread para escutar as mensagens
            t = Thread(target=escuta_coletor)
            t.setDaemon(True)
            t.start()
            # criacao da tela principal
            tela = TelaSistema()
            tela.Show()
        else:
            # cria janela de aviso para mostrar que nao foi possivel conectar
            janela_aviso = JanelaAviso(None, 'Nao foi possivel conectar ao coletor')
            janela_aviso.Center()
            janela_aviso.ShowModal()
            janela_aviso.Destroy()
        s_coletor_contectado.release()
    janela.Destroy()
    app.MainLoop()

# Por final, desconecta serviddor
finally:
    desconecta_coletor()
