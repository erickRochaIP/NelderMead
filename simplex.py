from PontoAvaliacao import PontoAvaliacao

class Simplex:

    def __init__(self, f, x0, lu):
        self.pontos = Simplex.criar_simplex(f, x0, lu)
        self.ordenar_simplex()


    # Recebe o eixo e o ponto inicial
    def criar_ponto(i, x0):
        return tuple(x0[j] if j != i else x0[j]+ 1 for j in range(len(x0)))

    # Recebe o ponto inicial
    # Retorna as bases e a origem
    def criar_pontos(x0):
        return [Simplex.criar_ponto(i, x0) for i in range(len(x0)+1)]

    # Recebe uma funcao e o ponto inicial
    # Retorna um simplex nao ordenado, no qual os pontos sao as bases e a origem
    def criar_simplex(f, x0, lu):
        return [PontoAvaliacao(p, f, lu) for p in Simplex.criar_pontos(x0)]

    # Recebe um simplex
    # Retorna o simplex ordenado por f(p)
    def ordenar_simplex(self):
        self.pontos.sort()

    # Recebe um simplex ordenado
    # Retorna o pior, segundo pior e melhor ponto
    def extrair_dados(self):
        return self.pontos[-1], self.pontos[-2], self.pontos[0]
    
    # Recebe um simplex ordenado e quantidade de dimensoes
    # Retorna o ponto centroide, excluindo o pior ponto
    def calcular_centroide(self):
        n = len(self.pontos) - 1
        return tuple(sum(p.x[i] for p in self.pontos[:-1]) / n for i in range(n))



    # Recebe simplex, um ponto e o valor de p nesse ponto
    # Retorna o simplex ordenado, tendo seu pior ponto substituido
    def substituir_pior_ponto(self, pa):
        self.pontos = self.pontos[:-1] + [pa]
        self.ordenar_simplex()


    # Recebe Simplex, quantidade de dimensoes, coeficiente de contracao e funcao
    # Retorna um Simplex contraido e ordenado
    def contrair_simplex(self, coef, f, lu):
        n = len(self.pontos) - 1
        S_contraido = []
        S_contraido.append(self.pontos[0])
        melhor = self.pontos[0]
        for i in range(1, n+1):
            ponto = self.pontos[i]
            ponto_deslocado = PontoAvaliacao.calcular_ponto_deslocado(ponto.x, melhor.x, coef)
            S_contraido.append(PontoAvaliacao(ponto_deslocado, f, lu))
        self.ordenar_simplex()

    def print_simplex(self):
        for pa in self.pontos:
            pa.print_ponto()
        print("================")

