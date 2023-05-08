# Recebe o eixo e a quantidade de dimensoes
def criar_ponto(i, n):
    return tuple(0 if j != i else 1 for j in range(n))

# Recebe a quantidade de dimensoes
# Retorna as bases e a origem
def criar_pontos(n):
    return [criar_ponto(i, n) for i in range(n+1)]

# Recebe uma funcao e a quantidade de dimensoes do dominio
# Retorna um simplex nao ordenado, no qual os pontos sao as bases e a origem
def criar_simplex(f, n):
    return [(p, f(p)) for p in criar_pontos(n)]

# Recebe um simplex
# Retorna o simplex ordenado por f(p)
def ordenar_simplex(S):
    return sorted(S, key=lambda x : x[1])

# Recebe um simplex ordenado
# Retorna o pior, segundo pior e melhor ponto
def extrair_dados(S):
    return S[-1], S[-2], S[0]

# Recebe um simplex ordenado e quantidade de dimensoes
# Retorna o ponto centroide, excluindo o pior ponto
def calcular_centroide(S, n):
    return tuple(sum(p[0][i] for p in S) / n for i in range(n))

# Recebe dois pontos e um coeficiente
# Retorna um ponto deslocado A + AB*coef
def calcular_ponto_deslocado(A, B, coef):
    return tuple(b*coef + a*(1 - coef) for a,b in zip(A, B))

# Recebe simplex, um ponto e o valor de p nesse ponto
# Retorna o simplex ordenado, tendo seu pior ponto substituido
def substituir_pior_ponto(S, novo_ponto, f_novo_ponto):
    return ordenar_simplex(S[:-1] + [(novo_ponto, f_novo_ponto)])


# Recebe Simplex, quantidade de dimensoes, coeficiente de contracao e funcao
# Retorna um Simplex contraido e ordenado
def contrair_simplex(S, n, coef, f):
    S_contraido = []
    S_contraido.append(S[0])
    melhor = S[0][0]
    for i in range(1, n+1):
        ponto = S[i][0]
        ponto_deslocado = calcular_ponto_deslocado(ponto, melhor, coef)
        S_contraido.append((ponto_deslocado, f(ponto_deslocado)))
    return ordenar_simplex(S_contraido)

def f(p):
    x, y = p[0], p[1]
    return (x - 10) ** 2 + (y - 20) ** 2

Simplex = criar_simplex(f, 2)
Simplex = ordenar_simplex(Simplex)
pior, segundo_pior, melhor = extrair_dados(Simplex)
print(Simplex)
print("Pior", pior)
print("Segundo pior", segundo_pior)
print("Melhor", melhor)
centroide = calcular_centroide(Simplex, 2)
print("Centroide", centroide)
refletido = calcular_ponto_deslocado(pior[0], centroide, 2)
print("Refletido", refletido)
f_refletido = f(refletido)
Simplex = substituir_pior_ponto(Simplex, refletido, f_refletido)
print(Simplex)

