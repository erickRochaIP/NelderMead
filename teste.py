from nelder_mead import nelder_mead
from scipy import optimize
import benchmark_functions as bf

def f2(p):
    x, y = p[0], p[1]
    return (x) ** 2 + (y + 20) ** 2

def f1(p):
    x = p[0]
    return x ** 2 + x * 3 + 10

# p, f_p = nelder_mead(f2, (0, -10), 500, params = {"ie": 4, "ic": 1/2, "ir": 2, "is": 1/2})
pa = nelder_mead(f2, (50, 50), 500,
                 [(-10, 10), (-10, 10)],
                 params = {"ie": 4, "ic": 1/2, "ir": 2, "is": 1/2})


# pa = nelder_mead(bf.zakharov_function, (50, 50), 500,
#                  [(-1, 1), (-1, 1)],
#                  params = {"ie": 4, "ic": 1/2, "ir": 2, "is": 1/2})

sp = optimize.minimize(f2, (50, 50),
                       bounds=[(-10, 10), (-10, 10)])

print("Ponto de minimo", pa.x)
print("Valor minimo", pa.f_x)
print("scipy", sp)
