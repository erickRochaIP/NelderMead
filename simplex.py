from PontoAvaliacao import PontoAvaliacao

class Simplex:

    def __init__(self, f, x0, lu):
        self.pontos = Simplex.criar_simplex(f, x0, lu)
        self.ordenar_simplex()


    # Recebe o eixo e o ponto inicial
    # Retorna ponto inicial + base do eixo
    # se o ponto nao possui o eixo, retorna o proprio ponto
    def criar_ponto(i, x0):
        return tuple(x0[j] if j != i else x0[j]+ 1 for j in range(len(x0)))

    # Recebe o ponto inicial
    # Retorna as bases e a origem
    def criar_pontos(x0):
        return [Simplex.criar_ponto(i, x0) for i in range(len(x0)+1)]

    # Recebe uma funcao, ponto inicial, limites das variaveis
    # Retorna um simplex ordenado, no qual os pontos sao ponto inicial + bases
    def criar_simplex(f, x0, lu):
        return [PontoAvaliacao(p, f, lu) for p in Simplex.criar_pontos(x0)]

    # Recebe um simplex
    # Ordena os pontos do simplex baseado na comparacao de PontoAvaliacao
    def ordenar_simplex(self):
        self.pontos.sort()

    # Recebe um simplex ordenado
    # Retorna o pior, segundo pior e melhor ponto
    def extrair_dados(self):
        return self.pontos[-1], self.pontos[-2], self.pontos[0]
    
    # Recebe um simplex ordenado
    # Retorna o ponto centroide, excluindo o pior ponto
    def calcular_centroide(self):
        n = len(self.pontos) - 1
        return tuple(sum(p.x[i] for p in self.pontos[:-1]) / n for i in range(n))

    # Recebe simplex ordenado, um ponto
    # Substitui pior ponto do simplex pelo ponto fornecido e ordena o simplex
    def substituir_pior_ponto(self, pa):
        self.pontos = self.pontos[:-1] + [pa]
        self.ordenar_simplex()

    # Recebe Simplex, coeficiente de encolhimento, funcao e limites das variaveis
    # Encolhe o Simplex e o ordena
    def contrair_simplex(self, coef, f, lu):
        n = len(self.pontos) - 1
        S_contraido = []
        S_contraido.append(self.pontos[0])
        melhor = self.pontos[0]
        for i in range(1, n+1):
            ponto = self.pontos[i]
            ponto_deslocado = PontoAvaliacao.calcular_ponto_deslocado(ponto.x, melhor.x, coef)
            S_contraido.append(PontoAvaliacao(ponto_deslocado, f, lu))
        self.pontos = S_contraido
        self.ordenar_simplex()

    def print_simplex(self):
        for pa in self.pontos:
            pa.print_ponto()
        print("================")

