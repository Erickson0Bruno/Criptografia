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
    #lê a mensagem criptografada
    curva.mensagem = leMensagemCrypt()
    
    curva.Pm = achaPm(curva)

    #Criptografa a mensagem
    # mensagemCrypt = cryptMensagem(curva)
    # print(mensagemCrypt[0])

    #salva em arquivo
    # salvaEmArquivo(mensagemCrypt)

def achaPm(curva):
    texto = curva.mensagem
    pmIntermediario = []
    AsciiTexto = ''
    for i in range(len(texto)):  
        #print(texto[i][1])
        kC1 =  multiplicacaoModular(curva.k, texto[i][0], curva.p, curva.d)
        kC1[1] = kC1[1]* (-1)
        
        pm = somaModular(texto[i][1], kC1, curva.p, curva.d)
        carac = divisaoMod(pm, curva.pontoEscolhido, curva.p, curva.d)
        AsciiTexto +=str(carac)
    print(AsciiTexto)
    return AsciiTexto
    
    
######################################################################

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

def divisaoMod(ponto, pontoEscolhido, p, d):
    aux = []
    
    aux.append(pontoEscolhido[0])
    aux.append( pontoEscolhido[1] * (-1))
    print(aux)
    print(pontoEscolhido)
    print(ponto)
    
    i = 0
    while ponto[0] != pontoEscolhido[0] and ponto[1] != pontoEscolhido[1]:
        i += 1
        ponto = somaModular(ponto, aux, p, d)
    print(i)
    return i
######################################################################################################3

def leMensagemCrypt():
    #lê os elementos do arquivo
    texto =[]
    
    arquivo = open('MensagemCriptografada.txt', 'r')
    conteudo = arquivo.read()
    arquivo.close()
    
    conteudo = conteudo.splitlines()
    
    for i in range(len(conteudo)):
        conteudo[i]= conteudo[i].replace('(', '').replace(')', '')

   
    for i in range(len(conteudo)):
        linha = conteudo[i].split(', ')
        
        C1 = []
        C2= []
        C1.append(int(linha[0]))
        C1.append(int(linha[1]))

    
        C2.append(int(linha[2]))
        C2.append(int(linha[3]))
        vetorC1C2 = []
        #vetorC1C2 fica assim vetorC1C2 = [C1][C2]
        vetorC1C2.append(C1)
        vetorC1C2.append(C2)
       
        texto.append(vetorC1C2)
        
    
    return texto

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
    PontoQ[0] = int(PontoQ[0])
    PontoQ[1] = int(PontoQ[1])
    PontoR[0] = int(float(PontoR[0]))
    PontoR[1] = int(float(PontoR[1]))
    return curva

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


main()