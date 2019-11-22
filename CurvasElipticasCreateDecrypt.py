class Curva:
    def __init__(self):
        self.d = 1
        self.e = 1 
        self.p = 23
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
    #print(curva.Pm)
    mensagemClara = transformaMensagem(curva.Pm)
    print(mensagemClara)
    
    #salva em arquivo
    salvaEmArquivo(mensagemClara)

def transformaMensagem(caracteres):
    linhaCarac = []
    #percorro a linha de tres em tres ja que o maior caracter da tab ascii tem 3 digitos
    for i in range(0, len(caracteres), 3):
        carac = caracteres[i:i+3]
        #se o primeiro elemento for apenas de preenchimento, ex: 910 o 9 e so pra preencher 3 digitos logo eu pego 10
        if carac[0] == '9':
            carac = carac[1:]
        #verifica se o elemento e null uma vez que o valor 0 e null na tabela ASCII
        if carac != '000':
            #concatena o caracter na linha da mensagem
            linhaCarac.append(chr(int(carac)))     
    #concatena na mensagem final
    return linhaCarac

def achaPm(curva):
    tamanhoBloco = len(str(curva.p)) - 1
    texto = curva.mensagem
    pmIntermediario = []
    AsciiTexto = ''
    
    #percorre os elementos da mensagem criptografada
    for i in range(len(texto)):  
        
        #calcula a chave 1 da mensagem criptografada k vezes
        kC1 =  multiplicacaoModular(curva.k, texto[i][0], curva.p, curva.d)
        # faz KC1 se tornar -KC1, que faz parte da formula
        kC1[1] = kC1[1]* (-1)
        
        #acha o valor de pm usando a subtracao (ou soma do inverso) do segundo elemento da mensagem criptografada [
        # com o primeiro elemento que eu acabei de calcular = kC1
        pm = somaModular(texto[i][1], kC1, curva.p, curva.d)

        #divido o pm resultante da etapa anterior pelo ponto Q, e obtenho o valor original do bloco
        carac = divisaoMod(pm, curva.pontoEscolhido, curva.p, curva.d)
        carac = str(carac)
        # aqui na hora de pegar o valor original se ele tiver um zero a esquerda, sendo ele um inteiro
        # o python elimina o zero  a esquerda, entao para concatenar de volta eu preciso do zero entao eu transformo para string e  
        # adiciono o zero de volta
        while len(carac)<tamanhoBloco:
            carac = '0'+ carac
        # concateno os blocos pra depois dividir de tres e tres, ja que a tab ascii tem 255 elementos portanto 3 digitos
        AsciiTexto +=str(carac)
    
    return AsciiTexto
    
    

######################################################################
#funcao de soma sobre a curva E23(1,1), a função recebe dois pontos P e Q e soma eles
#o calculo do Lambda, usado na funcao de soma é feito em uma função a parte
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
#funcao que faz a multiplicação sobre a curva E23(1,1), a funcao recebe um k, um ponto P e faz a soma de P + Q k vezes
#inserindo sempre resultado em P, lembrando que Q na primeira iteração tem o mesmo valor de P
def multiplicacaoModular(k, Ponto, p, d):
    #criptografa cada bloco
   
    P = Ponto
    Q = Ponto
    for i in range(int(k)): 
        P = somaModular(P, Q, p, d)  
        
    
    return P
#função que calcula o Lambda para ser usado na funcao de soma sob a curva E23(1,1)
#o calculo  do lambda e feito em partes, primeiro eu calculo a fração, separo o numerador e coloco na variavel a
# o denominador na variavel b, apos isso eu faço o calculo do inverso do modulo, chamando a funcao modulo passando o numerador a
# odenominador b o valor da curva no caso 23 e calculo o inverso do modulo. --- ((23 * n)+a) % 23 == 0  n tem que ser tal que 
# modo que o resultado da funcao seja 0, dai eu retorno o valor de Lambda
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
#calcula o valor de lambda de modo que ((23 * n)+a) % b seja  = 0 sendo n um numero inteiro.      
def modulo(a, b, p):
    cont = 0
    i = 0
    
    while True:
        i = 23*cont
        if (( i + a) % b) == 0:
            Lambda =  ( i + a ) / b
           
            return Lambda#( (p * cont) + a ) % b
        cont +=1

#faz a soma do iverso do ponto, ou seja soma o Ponto com o pontoQ(x, -y) ate o Ponto ser igual 
# ao ponto Q escolhido por ambas as partes na criação das chaves,
# o numero de vezes que eu precisei fazer isso sera o valor do meu bloco original.
def divisaoMod(ponto, pontoEscolhido, p, d):
    aux = []
    
    aux.append(pontoEscolhido[0])
    aux.append( pontoEscolhido[1] * (-1))
    # print(aux)
    # print(pontoEscolhido)
    # print(ponto)
    
    i = 0
    while ponto[0] != pontoEscolhido[0] and ponto[1] != pontoEscolhido[1]:
        i += 1
        ponto = somaModular(ponto, aux, p, d)
    
    return i
######################################################################################################3

#le a mensagem criptografada
def leMensagemCrypt():
    #lê os elementos do arquivo
    texto =[]
    arquivoMensagem = ''
    while arquivoMensagem == '':
        print('Informe o nome do arquivo que deseja ler a Mensagem')
        arquivoMensagem = input()
    arquivo = open(arquivoMensagem, 'r')
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
    
    chavePublica = ''

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
    chavePrivada = ''
    while chavePrivada == '':
        print('Informe o nome do arquivo que deseja ler a chave privada')
        chavePrivada = input()
    
    arquivo = open(chavePrivada, 'r')  
    conteudo = arquivo.readline()
    arquivo.close()

    curva.k= conteudo.split(', ')
    curva.k = int(curva.k[0])
    return curva

def salvaEmArquivo(mensagemDecrypt):
    aquivoMensagemDecrypt = ''
    while aquivoMensagemDecrypt == '':
        print('Informe o nome do arquivo que deseja salvar a Mensagem')
        aquivoMensagemDecrypt = input()

    arquivo = open(aquivoMensagemDecrypt, 'w')
    for i in range(len(mensagemDecrypt)):
        linha = ''
        for j in range(len(mensagemDecrypt[i])):
            linha += str(mensagemDecrypt[i][j])
        
        arquivo.write(linha)
    arquivo.close()
    print('\033[32m'+'Texto Descriptografado com Sucesso e salvo em '+ str(aquivoMensagemDecrypt)+'\033[0;0m')

   

main()