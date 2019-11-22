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
   
    #Limpa o console
    curva = Curva()   
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

    # função que calcula os pontos da curva E23(1,1)
    curva = encontraListaPontos(curva)
    PrintaParametros(curva)
    curva = escolhePonto(curva)
    curva = escolheK(curva)
    curva.pontoR = multiplicacaoModular(curva.k, curva.pontoEscolhido, curva.p, curva.d)#calculaR(curva)
   
    salvaEmArquivo(curva)
    
#funcao para escolher o valor da chave privada do usuario
def escolheK(curva): 
    k = -1
    while k < 1:
        print('Informe o Parâmetro k maior que 0')
        k = int(input())
    curva.k = k
    return curva


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
    print("K= ", k, " Ponto= ", Ponto)
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

######################################################################################################3
#Escolhe um ponto Q que esta contido na lista de pontos da curva, 
# se o ponto informado nao estiver na lista ele pede para informar de novo
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

    
# função que calcula os pontos da curva E23(1,1) para posteriormente o usuario escolher um ponto Q
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


# Apemas imprime os Parametros p, d, e e alista de pontos pro usuario escolher
def PrintaParametros(curva):
    print('\033[32m'+'Parâmetro d = '+str(curva.d)+' Parâmetro e = '+str(curva.e)+' Parâmetro p = '+str(curva.p)+'\033[0;0m')
    print('\033[32m'+'Lista de Pontos '+ str(curva.pontos)+'\033[0;0m')

#Salva em arquivo as chaves publica e privada  
def salvaEmArquivo(curva):
    #funcao que salva em arquivo
    print("CURVA valores k=",curva.k,  " e=",  curva.e, " d=", curva.d," p=",  curva.p, "R=", curva.pontoR)
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