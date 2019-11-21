class Curva:
    def __init__(self):
        self.d = 0
        self.e = 0 
        self.p = 0
        self.k = 0
        self.pontos = []
        self.pontoEscolhido = []
        self.pontoR = []
        self.Pm = []
        self.mensagem = []


def main():
    curva = Curva()
    #le chave publica
    curva = leChavePublica(curva)
    curva = leChavePrivada(curva)
    print("C", curva.d, curva.e, curva.p)
    print("chave publica", curva.pontoR)
    print("chave privada", curva.k)
    #lê a mensagem Clara
    curva.mensagem = leMensagemClara()
    print(curva.mensagem)
    curva.Pm = achaPm(curva)
    print(curva.Pm)
    #Criptografa a mensagem
    mensagemCrypt = cryptMensagem(curva)
    #print(mensagemCrypt[0])

    #salva em arquivo
    salvaEmArquivo(mensagemCrypt)

def cryptMensagem(curva):
    kQ = multiplicacaoModular(curva.k, curva.pontoEscolhido, curva.p, curva.d)
    kR = multiplicacaoModular(curva.k, curva.pontoR, curva.p, curva.d)
    final = []
    for i in range(len(curva.Pm)):
        for j in range(len(curva.Pm[i])):
            
            pmKr = somaModular(curva.Pm[i][j], kR, curva.p, curva.d)
            final.append((kQ,pmKr))
    return final

def achaPm(curva):
    PM = []
    textoClaro = curva.mensagem
    
    M = (len(str(curva.p)) -1)
    
    cont =0
    #percorre as linhas da matriz contendo o texto
    for i in range(len(textoClaro)):
        linha = ''
        #le cada caracter da linha
        for j in range(len(textoClaro[i])):
            #transforma o caracter no valor correspondente da tabela ASCII
            caracter = str(ord(textoClaro[i][j]))
            #verifica o valor possui 3 digitos
            if len(caracter) == 3:
                #se tem 3 digitos adiciona na linha para depois ser dividido em bloco
                linha+=(str(caracter))

            #verifica se o valor tem 2 digitos
            if len(caracter) == 2:
                #se tem 2 digitos adiciono 9 na frente para tornar o elemento homogêneo com 3 digitos  e concateno na linha
                linha += '9'+ str(caracter)
            #verifica se o valor tem 1 digito
            if len(caracter) == 1:
                #se tem 1 digito adiciono 90 na frente para tornar o elemento homogêneo com 3 digitos e concateno na linha 
                linha += '90'+ str(caracter)
        #chamo a função CalculaPm para criptografar a mensagem
        PM.append(CalculaPm(linha, M, curva))
    #print(PM)
    #retorna Pm
    return PM


def CalculaPm(linha, M, curva):
    #verifico se a linha tem a quantidade de digitos multipla de M(chave N-1)
    concat = len(linha) % M
    if concat != 0:
        #se nao for multiplo de M(chave N-1) adiciono 0 ate a quantidade de digitos ser multiplo de M
        for i in range(M - concat):
            linha+= "0"
    retorno = []
    print(linha)
    #Percorre a linha de M em M valores  
    for w in range(0, len(linha), M):
        #criptografa a linha em blocos de tamanho M
        print(linha[w:w+M])
        retorno.append(multiplicacaoModular(linha[w:w+M], curva.pontoEscolhido, curva.p, curva.d))
    
    #retorna o resultado
    return retorno

######################################################################
def somaModular(PontoP, PontoQ, p, d):
    
    P = PontoP
    Q = PontoQ
    Lambda  = calculaLambda(P, Q, d, p)
    if not Lambda:
        return [0,0]
    xr = ( (Lambda**2) - P[0] - Q[0]) % p
    yr = ( Lambda * ( P[0] - xr) - P[1]) % p 
    P = [int(xr), int(yr)]
    return P

def multiplicacaoModular(k, Ponto, p, d):
    #criptografa cada bloco
   
    P = Ponto
    Q = Ponto
    for i in range(int(k)): 
        P = somaModular(P, Q, p, d)  
        
    
    return P

def calculaLambda(pontoP, pontoQ, d, p):
    
    if pontoP[0] == pontoQ[0] and pontoP[1] == pontoQ[1]:
        #formula de lambda para P = Q
        if pontoP[1] != 0:
            a = (3 * (pontoP[0]**2)+d)
            b = (2 * pontoP[1])
            return modulo(a, b, p)
        
    elif pontoP[0] != pontoQ[0]:
        #Ponto
        a = (pontoQ[1] - pontoP[1]) 
        b = (pontoQ[0] - pontoP[0])
        return modulo(a, b, p)
    return False
def modulo(a, b, p):
    cont = 0
    i = 0
    
    while True:
        i = 23*cont
        if (( i + a) % b) == 0:
            Lambda =  ( i + a ) / b
           
            return Lambda#( (p * cont) + a ) % b
        cont +=1
######################################################################################################3



def leMensagemClara():
    texto =[]
    arquivoMensagem = 'a.txt'

    while arquivoMensagem == '':
        print('Informe o nome do arquivo que deseja ler a Mensagem clara')
        arquivoMensagem = input()

    #função que lê a Mensagem do aquivo mensagemClara.txt
    arquivo = open(arquivoMensagem, 'r')
    conteudo = arquivo.read()
    arquivo.close()
    texto = conteudo.splitlines()

    return texto


def leChavePrivada(curva):
    chavePrivada = 'aliceprivate.txt'
    while chavePrivada == '':
        print('Informe o nome do arquivo que deseja ler a chave privada')
        chavePrivada = input()
    
    arquivo = open(chavePrivada, 'r')  
    conteudo = arquivo.readline()
    arquivo.close()

    curva.k= conteudo.split(', ')
    curva.k = int(curva.k[0])
    return curva

def leChavePublica(curva):
    #função que le a chave Publica do arquivo chavePublica.txt

    chavePublica = 'alicepublic.txt'

    while chavePublica == '':
        print('Informe o nome do arquivo que deseja ler a chave publica')
        chavePublica = input()
    
    arquivo = open(chavePublica, 'r')  
    conteudo = arquivo.readline()
    arquivo.close()
    PontoQ = ['', '']
    PontoR = ['', '']
    curva.d, curva.e, curva.p, PontoQ[0], PontoQ[1], PontoR[0], PontoR[1] = conteudo.split(', ')
    curva.pontoEscolhido = PontoQ
    curva.pontoR = PontoR

    #apenas transforma de string para os respectivos formatos 
    curva.d = int(curva.d)
    curva.e = int(curva.e)
    curva.p = int(curva.p)
    PontoQ[0] = float(PontoQ[0])
    PontoQ[1] = float(PontoQ[1])
    PontoR[0] = float(PontoR[0])
    PontoR[1] = float(PontoR[1])
    return curva

def salvaEmArquivo(mensagemCrypt):
    #funcao que salva em arquivo
    arquivo = open('MensagemCriptografada.txt', 'w')
    for i in range(len(mensagemCrypt)):
        linha = mensagemCrypt[i]
        linha = str(linha)
        linha = linha.replace('[', '')        
        linha = linha.replace(']', '')
        linha +='\n'
        
        arquivo.write(linha)
    arquivo.close()
    print('\033[32m'+'Texto Criptografado com Sucesso'+'\033[0;0m')

main()