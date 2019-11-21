class Curva:
    def __init__(self):
        self.d = 0
        self.e = 0 
        self.p = 0
        self.k = 0
        self.pontos = []
        self.pontoEscolhido = []
        self.pontoR = []

def main():
   
    curva = Curva()

    curva = recebeParametros(curva)

    #Limpa o console
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    curva = encontraListaPontos(curva)
    PrintaParametros(curva)
    curva = escolhePonto(curva)
    curva = escolheK(curva)
    curva = multiplicacaoModular(curva.k, curva.pontoEscolhido, curva.p, curva.d)#calculaR(curva)
    salvaEmArquivo(curva)
    print(curva.pontoR)

def escolheK(curva): 
    k = -1
    while k < 1:
        print('Informe o Parâmetro k maior que 0')
        k = int(input())
    curva.k = k
    return curva


######################################################################
def somaModular(PontoP, PontoQ, p, d):
    
    P = PontoP
    Q = PontoQ
    Lambda  = calculaLambda(P, Q, d, p)
    
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
        a = (3 * (int(pontoP[0])**2))
        b = (2 * pontoP[1])
        return modulo(a, b, p)
    else:
        #Ponto
        a = (pontoQ[1] - pontoP[1]) 
        b = (pontoQ[0] - pontoP[0])
        return modulo(a, b, p)

def divisaoMod(ponto, pontoEscolhido, p, d):
    aux = []
    
    aux.append(pontoEscolhido[0])
    aux.append( pontoEscolhido[1] * (-1))
    # print(aux)
    # print(pontoEscolhido)
    
    i = 0
    while ponto[0] != pontoEscolhido[0] and ponto[1] != pontoEscolhido[1]:
       
        i += 1
        # print(ponto)
        ponto = somaModular(ponto, aux, p, d)
    print(i)
    return i

def modulo(a, b, p):
    cont = 1
    
    if b<0:
        b = b*(-1)
    
    while True:
        if b==0:
            b = 1
        if (( (p * cont) + a) % b) == 0:
            Lambda =  ( (p * cont) + a ) / b
            
            return Lambda#( (p * cont) + a ) % b
        cont +=1


######################################################################################################3


# ######################################################################
# def calculaR(curva):
#     P = curva.pontoEscolhido
#     Q = curva.pontoEscolhido
#     for i in range(curva.k):
#         Lambda  = calculaLambda(P, Q, curva.d, curva.p)
#         xr = ( (Lambda**2) - P[0] - Q[0]) % curva.p
#         yr = ( Lambda * ( P[0] - xr) - P[1]) % curva.p 
#         P = [xr, yr]

#     curva.pontoR = P 
#     return curva   

# def funcModulo(x):
#     return ''

# def calculaLambda(pontoP, pontoQ, d, p):
#     if pontoP[0] == pontoQ[0] and pontoP[1] == pontoQ[1]:
#         #formula de lambda para P = Q
#         a = (3 * (pontoP[0]**2))
#         b = (2 * pontoP[1])
#         return modulo(a, b, p)
#     else:
#         #Ponto
#         a = (pontoQ[1] - pontoP[1]) 
#         b = (pontoQ[0] - pontoP[0])
#         return modulo(a, b, p)

# def modulo(a, b, p):
#     cont = 1
#     print('a: '+ str(a)+ ' b: '+ str(b))
        
#     while True:
#         print(cont)
#         if (( (p * cont) + a) % b) == 0:
#             Lambda =  ( (p * cont) + a ) / b
#             print('Lambda: '+str(Lambda))
#             return Lambda#( (p * cont) + a ) % b
#         cont +=1
######################################################################################################3

def escolhePonto(curva):
    ponto = []
    while ponto not in curva.pontos:
        print('Escolha o ponto desejado a partir dos porntos acima listados')
        print('Informe o valor da cordenada x')
        x = int(input())
        print('Informe o valor da cordenada y')
        y =  int(input())
        ponto = [x, y]
    curva.pontoEscolhido = ponto
    return curva

    

def encontraListaPontos(curva):
    
    for i in range(curva.p):
        ponto = []
        py = (i**2)%curva.p
        for j in range(curva.p):
            px = ((j**3) + curva.d*j + curva.e)% curva.p
            if px == py:
                ponto = [j, i]
               
                if ponto not in curva.pontos:
                    curva.pontos.append(ponto)
    curva.pontos.sort()
    return curva



def PrintaParametros(curva):
    print('\033[32m'+'Parâmetro d = '+str(curva.d)+' Parâmetro e = '+str(curva.e)+' Parâmetro p = '+str(curva.p)+'\033[0;0m')
    print('\033[32m'+'Lista de Pontos '+ str(curva.pontos)+'\033[0;0m')
def recebeParametros(curva):
    '''
    #Recebe o Parametro 'd'
    print('Informe o Parâmetro d maior que 0')
    d = int(input())
    while d < 1:
        print('Informe o Parâmetro d maior que 0')
        d = int(input())
    curva.d = d

    #Recebe o parametro 'e'
    print('Informe o Parâmetro e maior que 0')
    e = int(input())
    while e < 1:
        print('Informe o Parâmetro e maior que 0')
        e = int(input())
    curva.e = e

    #Recebe o Parametro 'p'
    print('Informe o Parâmetro p maior que 0')
    p = int(input())
    while d < 1:
        print('Informe o Parâmetro p maior que 0')
        p = int(input())
    curva.p = p
'''
    curva.d = 1
    curva.e = 1
    curva.p = 23
    return curva

def salvaEmArquivo(curva):
    #funcao que salva em arquivo

    #Salva chave Pública
    chavePublica = ''

    while chavePublica == '':
        print('Informe o nome do arquivo que deseja salvar a chave publica')
        chavePublica = input()
    
    arquivo = open(chavePublica, 'w')
    linha = str(curva.d) +', '+ str(curva.e )+ ', ' + str(curva.p)+', '+str(curva.pontoEscolhido[0]) + ', '+ str(curva.pontoEscolhido[1])+ ', ' +str(curva.pontoR[0])+', '+str(curva.pontoR[1])
    
    arquivo.write(linha)
    arquivo.close()

    #Salva chave privada
    chavePrivada = ''

    while chavePrivada == '':
        print('Informe o nome do arquivo que deseja salvar a chave privada')
        chavePrivada = input()
    
    arquivo = open(chavePrivada, 'w')
    arquivo.write(str(curva.k))
    arquivo.close()
    print('\033[32m'+'Chaves salvas com Sucesso'+'\033[0;0m')


main()