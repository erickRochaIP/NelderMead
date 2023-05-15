class PontoAvaliacao:

    def __init__(self, x, f, lu):
        self.x = x
        self.inviabilidade = PontoAvaliacao.obter_inviabilidade_ponto(x, lu)
        self.f_x = f(x) if self.inviabilidade == 0 else None

    def obter_inviabilidade_ponto(x, lu):
        return sum(PontoAvaliacao.obter_inviabilidade_var(xi, lui) for xi, lui in zip(x, lu))
    
    def obter_inviabilidade_var(xi, lui):
        li, ui = lui[0], lui[1]
        return max(0, li - xi) + max(0, xi - ui)
    
    def __lt__(self, other):
        if self.inviabilidade != other.inviabilidade:
            return self.inviabilidade < other.inviabilidade
        elif self.inviabilidade != 0:
            return False
        else:
            return self.f_x < other.f_x
        
    def __le__(self, other):
        if self.inviabilidade != other.inviabilidade:
            return self.inviabilidade < other.inviabilidade
        elif self.inviabilidade != 0:
            return True
        else:
            return self.f_x <= other.f_x
        
    def __gt__(self, other):
        if self.inviabilidade != other.inviabilidade:
            return self.inviabilidade > other.inviabilidade
        elif self.inviabilidade != 0:
            return False
        else:
            return self.f_x > other.f_x
        
    def __ge__(self, other):
        if self.inviabilidade != other.inviabilidade:
            return self.inviabilidade > other.inviabilidade
        elif self.inviabilidade != 0:
            return True
        else:
            return self.f_x >= other.f_x
    
    def __eq__(self, other):
        return self.inviabilidade == other.inviabilidade and self.f_x == other.f_x
        
