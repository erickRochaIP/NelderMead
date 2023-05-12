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
    return tuple(sum(p[0][i] for p in S[:-1]) / n for i in range(n))

# Recebe dois pontos e um coeficiente
# Retorna um ponto deslocado A + AB*coef
def calcular_ponto_deslocado(A, B, coef, f):
    p = tuple(b*coef + a*(1 - coef) for a,b in zip(A, B))
    return p, f(p)

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
        ponto_deslocado = calcular_ponto_deslocado(ponto, melhor, coef, f)
        S_contraido.append(ponto_deslocado)
    return ordenar_simplex(S_contraido)


# Recebe uma funcao, quantidade de dimensoes, quantidade de iteracoes e os parametros
# Retorna o ponto de minimo da funcao
def nelder_mead(f, n, avals, params):
	# TODO: Receber ponto inicial e params
    Simplex = criar_simplex(f, n)
    Simplex = ordenar_simplex(Simplex)
    pior, segundo_pior, melhor = extrair_dados(Simplex)

    while avals > 0:
        avals -= 1
        centroide = calcular_centroide(Simplex, n)
        refletido = calcular_ponto_deslocado(pior[0], centroide, 2, f)
        if segundo_pior[1] > refletido[1] >= melhor[1]:
            Simplex = substituir_pior_ponto(Simplex, refletido[0], refletido[1])
            pior, segundo_pior, melhor = extrair_dados(Simplex)
            continue
        if melhor[1] > refletido[1]:
            expandido = calcular_ponto_deslocado(pior[0], centroide, 4, f)
            if refletido[1] > expandido[1]:
                Simplex = substituir_pior_ponto(Simplex, expandido[0], expandido[1])
            else:
                Simplex = substituir_pior_ponto(Simplex, refletido[0], refletido[1])
            pior, segundo_pior, melhor = extrair_dados(Simplex)
            continue
        if pior[1] >= refletido[1]:
            contraido_externo = calcular_ponto_deslocado(pior[0], centroide, 3/2, f)
            if refletido[1] > contraido_externo[1]:
                Simplex = substituir_pior_ponto(Simplex, contraido_externo[0], contraido_externo[1])
                pior, segundo_pior, melhor = extrair_dados(Simplex)
                continue
        else:
            contraido_interno = calcular_ponto_deslocado(pior[0], centroide, 1/2, f)
            if pior[1] > contraido_interno[1]:
                Simplex = substituir_pior_ponto(Simplex, contraido_interno[0], contraido_interno[1])
                pior, segundo_pior, melhor = extrair_dados(Simplex)
                continue

        Simplex = contrair_simplex(Simplex, n, 1/2, f)
        pior, segundo_pior, melhor = extrair_dados(Simplex)

    return melhor
