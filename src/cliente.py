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


# Classe que representa a janela para inserir os dados para cadastrar uma maquina
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


# Classe que representa a janela para inserir os dados para coletar um determinad recurso
class JanelaColetaRecurso(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaColetaRecurso, self).__init__(parent, -1, 'Coleta de Recurso Monitorado',
                                                  style=style)
        # Configuracao de elementos de tela
        self.ip_maquina_texto = wx.StaticText(self, -1, "Digite o IP da maquina monitorada")
        self.ip_maquina = wx.TextCtrl(self, value="")
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

    # funcao para pegar os dados inseridos na janela
    def pega_recurso_escolhido(self):
        return str(self.ip_maquina.GetValue()) + ',' + \
               str(self.escolhe_recurso.GetSelection()) + ',' + \
               str(self.quantidade.GetValue())


# Classe que representa a janela para mostra a lista de maquinas cadastradas
class JanelaListaMaquinasCadastradas(wx.Dialog):
    def __init__(self, parent, listagem_maquinas):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaListaMaquinasCadastradas, self).__init__(parent, -1, 'Listagem de maquinas cadastradas',
                                                             style=style)
        # Configuracao de elementos de tela
        listagem_maquinas = listagem_maquinas.replace('lista,', '').split(',')
        tabela = gridlib.Grid(self, size=(320, 300))
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


# Classe que representa a janela para mostra as informacoes de um determinado recurso coletado
class JanelaRecursosColetados(wx.Dialog):
    def __init__(self, parent, recurso_coletado):
        recurso_coletado = recurso_coletado.split(',')

        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaRecursosColetados, self).__init__(parent, -1, str('Recurso coletado - ' + recurso_coletado[1]),
                                                      style=style)
        # Configuracao de elementos de tela
        self.recurso_texto = wx.TextCtrl(self, -1, str(recurso_coletado[2]),
                                         style=wx.TE_MULTILINE | wx.BORDER_SUNKEN | wx.TE_READONLY |
                                               wx.TE_RICH2, size=(400, 400))

        botoes = self.CreateButtonSizer(wx.OK)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.recurso_texto, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)


# Classe que representa a tela principal
class TelaSistema(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="SysMonitorUFF", size=(450, 200))

        # Configuracao de elementos de tela
        self.panel = wx.Panel(self)

        # Configuracoes de textos, botoes e os eventos de clique dos botoes
        self.bem_vindo = wx.StaticText(self.panel, label="Bem vindo ao Sistema de Monitoramento de Maquinas - UFF", )
        self.botao_cadastrar_maquina = wx.Button(self.panel, label="Cadastrar Maquina", size=(250, 30))
        self.Bind(wx.EVT_BUTTON, botao_cadastrar_maquina, self.botao_cadastrar_maquina)

        self.botao_listar_maquinas = wx.Button(self.panel, label="Listar Maquinas Cadastradas", size=(250, 30))
        self.Bind(wx.EVT_BUTTON, botao_listar_maquinas, self.botao_listar_maquinas)

        self.botao_coletar_recurso = wx.Button(self.panel, label="Coletar Recurso", size=(250, 30))
        self.Bind(wx.EVT_BUTTON, botao_coletar_recurso, self.botao_coletar_recurso)

        self.botao_sair = wx.Button(self.panel, label="Sair", size=(250, 30))
        self.Bind(wx.EVT_BUTTON, botao_sair, self.botao_sair)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.bem_vindo, 0, wx.CENTER | wx.ALL, 5)
        vbox.Add(self.botao_cadastrar_maquina, 0, wx.CENTER | wx.ALL, 5)
        vbox.Add(self.botao_listar_maquinas, 0, wx.CENTER | wx.ALL, 5)
        vbox.Add(self.botao_coletar_recurso, 0, wx.CENTER | wx.ALL, 5)
        vbox.Add(self.botao_sair, 0, wx.CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

    # funcao que cria uma janela de aviso
    def mostra_janela_aviso(self, aviso):
        j_aviso = JanelaAviso(None, aviso)
        j_aviso.Center()
        j_aviso.ShowModal()
        j_aviso.Destroy()

    # funcao que mostra janela de aviso com mensagem de erro
    def mostra_erro(self):
        self.mostra_janela_aviso('Ocorreu um erro')

    # funcao que mostra janela de aviso com mensagem de resposta ao cadastro
    def mostra_cadastro(self, msg):

        if 'NOk' in msg:
            self.mostra_janela_aviso('Nao foi possivel cadastrar maquina')
        else:
            self.mostra_janela_aviso('Maquina cadastrada com sucesso')

    # funcao que mostra janela que lista as maquinas cadastradas ou janela de aviso caso nao tenha nenhuma
    def mostra_lista_maquinas(self, msg):

        if msg == 'lista,':
            self.mostra_janela_aviso('Nenhuma maquina cadastrada')
        else:
            j_lista_maquinas = JanelaListaMaquinasCadastradas(None, msg)
            j_lista_maquinas.Center()
            j_lista_maquinas.ShowModal()
            j_lista_maquinas.Destroy()

    # funcao que mostra janela que apresenta as informacoes de um recurso coletado ou janela de aviso caso tenha erro
    def mostra_recurso(self, msg):

        if 'NOk' in msg:
            self.mostra_janela_aviso('Nao foi possivel conectar a maquina')
        else:
            j_lista_maquinas = JanelaRecursosColetados(None, msg)
            j_lista_maquinas.Center()
            j_lista_maquinas.ShowModal()
            j_lista_maquinas.Destroy()


# funcao de evento de clique do botao para cadastrar maquina
def botao_cadastrar_maquina(evento):
    global s_operacao_atual, operacao_atual

    # criacao da janela de cadastro de maquina
    janela = JanelaCadastrarMaquina(None)
    janela.Center()
    dados = None
    if janela.ShowModal() == wx.ID_OK:
        # apos clicar em OK da janela, pega as informacoes inseridas na janela
        dados = janela.pegar_ip_maquina()
    janela.Destroy()

    if dados is not None:
        # envia mensagem de cadastro para o coletor
        envia_mensagem_coletor(str('cadastra,' + dados))


# funcao de evento de clique do botao para listar as maquinas cadastradas
def botao_listar_maquinas(evento):
    # envia mensagem para listar maquinas cadastradas para o coletor
    envia_mensagem_coletor('lista')


# funcao de evento de clique do botao para coletar um recurso
def botao_coletar_recurso(evento):
    # criacao da janela de coleta de recurso
    janela = JanelaColetaRecurso(None)
    janela.Center()
    dados = None
    if janela.ShowModal() == wx.ID_OK:
        # apos clicar em OK da janela, pega as informacoes inseridas na janela
        dados = janela.pega_recurso_escolhido()
    janela.Destroy()

    if dados is not None:
        # envia mensagem de coleta de recurso para o coletor
        envia_mensagem_coletor(str('recurso,' + dados))

# funcao de evento de clique do botao para sair
def botao_sair(evento):
    global tela
    # fecha a tela principal
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
def configura_coletor(ip, port):
    global coletor_ip, coletor_porta
    coletor_ip = ip
    coletor_porta = port


# Funcao que conecta socket do coletor
def conecta_coletor():
    global coletor_sock
    try:
        # Cria socket para conexao
        coletor_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configura endereco - IP e Porta
        endereco_coletor = (coletor_ip, coletor_porta)
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
def estabelece_conexao_coletor(coletor_ip, coletor_porta):
    global s_coletor_contectado, coletor_conectado, mensagem_erro

    # Configura IP e Porta do coletor
    configura_coletor(coletor_ip, coletor_porta)
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

        # filtra qual tipo de mensagem de retorna e chama a funcao da tela principal
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

# variaveis para guardar informacoes de ip e porta do coletor
coletor_ip = ''
coletor_porta = None
# Declaracao do socket de conexao com coletor
coletor_sock = None
coletor_conectado = False
s_coletor_contectado = BoundedSemaphore()

# tela principal
tela = None

try:

    # cria interface grafica
    app = wx.App(False)

    # cria janela com dados do coletor
    janela = JanelaDadoColetor(None)
    janela.Center()
    if janela.ShowModal() == wx.ID_OK:
        # pega informacoes de ip e porta do coletor
        dados_coletor = janela.pegar_dados_coletor().split(',')
        coletor_ip = dados_coletor[0]
        coletor_porta = int(dados_coletor[1])
        # coneta com coletor
        estabelece_conexao_coletor(coletor_ip, coletor_porta)
        s_coletor_contectado.acquire()
        if coletor_conectado:
            # executa thread para escutar as mensagens do coletor
            t = Thread(target=escuta_coletor)
            t.setDaemon(True)
            t.start()
            # criacao da tela principal
            tela = TelaSistema()
            tela.Center()
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

# Por final, desconecta do coletor
finally:
    desconecta_coletor()
