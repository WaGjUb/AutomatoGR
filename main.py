import sys

#classe para a criaçaõ da arvore
class node(object):
    def __init__(self, data, son = []):
        self.data = data
        self.son = son 

class arquivo(object):

    #leitura do arquivo
    def __init__(self):
            self.linhas = [linha.rstrip('\n\r') for linha in open(sys.argv[1])]

            
    #retornos
    def retConfiguracoes(self):
        self.configuracoes = []
        for i in range(3,len(self.linhas),1):
            self.configuracoes.append(self.linhas[i])
    #    print(self.configuracoes[1])
        return self.configuracoes
    
    def retTerminais(self):
        self.terminais = self.linhas[0].split(' ')
        return self.terminais

    def retVariaveis(self):
        self.variaveis = self.linhas[1].split(' ')
        return self.variaveis    

    def retInicial(self):
        self.inicial = self.linhas[2].split(' ')
        return self.inicial

    def retDigitado(self):
        return sys.argv[2]
    
class gerador(object):
   
    def __init__(self,arquivo):
        self.arquivo = arquivo
                       
    def verifica(self, palavra):
        if self.arquivo.retDigitado() == palavra:
            sys.stdout.flush()
            if palavra == "":
                print("\nA palavra vazia é válida nesta gramatica")
            else:
                print("\nA palavra "+palavra+" é válida nesta gramatica")
            return exit()
        else:
            return False

    def geraPalavra(self, palavraInicio):
        self.Geradas = []
        tmpList = []
        dump = ''
        ver = True
      #  import pdb
      #  pdb.set_trace()
        for i in palavraInicio: #anda pelos caracteres da palavra
            for conf in self.arquivo.retConfiguracoes(): #anda em todas as configuracos para cada caractere da palavra
                if conf[0] == i:
                    ver = False
                    if conf[2:] == "epsilon":
                        conf = conf[:2]
                    if len(self.Geradas) != 0:
                        for geradas in range(len(self.Geradas)):
                            aux = self.Geradas[geradas]
                            tmpList.append(aux + dump + conf[2:])
                    else:
                        tmpList.append(dump + conf[2:])
                        
            if ver == False:    
                self.Geradas = tmpList[:]
                tmpList = []
                ver = True
                dump = ''
            else:
                dump += i

        if len(self.Geradas) == 0:
            self.Geradas.append(dump)
        else:
            for idx in range(len(self.Geradas)):
                self.Geradas[idx] += dump
        return self.Geradas

    def bruteForce(self):
        lista = []
        lista.append(self.geraPalavra(self.arquivo.retInicial()))
        soma = 0
        time = 0
        while True:
            tam = len(lista)
            for i in range(len(lista)):
                for elemento in lista[i]:
                    soma += 1
                    if soma >= 100000:
                        time += 1
                        sys.stdout.flush()
                        print("\nJá foram geradas "+ str(time * soma) + " palavras")
                        string = input("Deseja continuar? ")
                        if string == "n":
                            print("Programa finalizado pelo usuário")
                            exit()
                        else:
                            soma = 0
                    print(elemento, end = "\r")
                    self.verifica(elemento)
                    lista.append(self.geraPalavra(elemento))
            for apaga in range(tam):
                lista.pop(0)


if __name__ == "__main__":

    #verifica os parametros
    if len(sys.argv) != 3:
        if len(sys.argv) < 2:
            print("O arquivo de leitura deve ser passado como parametro")
            exit()
        else:
            sys.argv.append("")
            print("Palavra vazia passada como parâmetro!")
    g = gerador(arquivo())
    g.bruteForce()
    
    
#    tree = node("grandmother", [node("filho1"), node("filho2")])
 #   tree.son[0].son = [node("haha")]
#   print(len(tree.son[0].data))
