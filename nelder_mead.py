from simplex import Simplex
from PontoAvaliacao import PontoAvaliacao

# Recebe uma funcao, ponto inicial, quantidade de iteracoes e os parametros
# Retorna o ponto de minimo da funcao
def nelder_mead(f, x0, avals, lu, params = None):
    if params is None:
        params = {}
    coef_reflexao = params["ir"] if "ir" in params else 2
    coef_exp = params["ie"] if "ie" in params else 4
    coef_contracao = params["ic"] if "ic" in params else 1/2
    coef_encolhimento = params["is"] if "is" in params else 1/2

    S = Simplex(f, x0, lu)
    pior, segundo_pior, melhor = S.extrair_dados()

    while avals > 0:
        # S.print_simplex()

        avals -= 1
        centroide = S.calcular_centroide()
        refletido = PontoAvaliacao.calcular_ponto_deslocado(pior.x, centroide, coef_reflexao)
        refletido = PontoAvaliacao(refletido, f, lu)
        if segundo_pior > refletido >= melhor:
            S.substituir_pior_ponto(refletido)
            pior, segundo_pior, melhor = S.extrair_dados()
            continue
        if melhor > refletido:
            expandido = PontoAvaliacao.calcular_ponto_deslocado(pior.x, centroide, coef_exp)
            expandido = PontoAvaliacao(expandido, f, lu)
            if refletido > expandido:
                S.substituir_pior_ponto(expandido)
            else:
                S.substituir_pior_ponto(refletido)
            pior, segundo_pior, melhor = S.extrair_dados()
            continue
        if pior >= refletido:
            contraido_externo = PontoAvaliacao.calcular_ponto_deslocado(pior.x, centroide, coef_reflexao - coef_contracao)
            contraido_externo = PontoAvaliacao(contraido_externo, f, lu)
            if refletido > contraido_externo:
                S.substituir_pior_ponto(contraido_externo)
                pior, segundo_pior, melhor = S.extrair_dados()
                continue
        else:
            contraido_interno = PontoAvaliacao.calcular_ponto_deslocado(pior.x, centroide, coef_contracao)
            contraido_interno = PontoAvaliacao(contraido_interno, f, lu)
            if pior > contraido_interno:
                S.substituir_pior_ponto(contraido_interno)
                pior, segundo_pior, melhor = S.extrair_dados()
                continue

        S.contrair_simplex(coef_encolhimento, f, lu)
        pior, segundo_pior, melhor = S.extrair_dados()

    return melhor
