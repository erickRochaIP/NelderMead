from nelder_mead import nelder_mead

def f2(p):
    x, y = p[0], p[1]
    return (x + 10) ** 2 + (y + 20) ** 2

def f1(p):
    x = p[0]
    return x ** 2 + x * 3 + 10

p, f_p = nelder_mead(f2, [0, -10], 500)

print("Ponto de minimo", p)
print("Valor minimo", f_p)
