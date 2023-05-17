from nelder_mead import nelder_mead
from scipy import optimize
import benchmark_functions as bf

def f2(p):
    x, y = p[0], p[1]
    return (x) ** 2 + (y + 20) ** 2

def f1(p):
    x = p[0]
    return x ** 2 + x * 3 + 10

functions = [bf.zakharov_function,
             bf.rosenbrock_function,
             bf.expanded_schaffer_function,
             bf.rastrigin_function,
             bf.levy_function]

def test_function(f, x0, lu):
    p_nm = nelder_mead(f, x0, 500,
                 lu,
                 params = {"ie": 4, "ic": 1/2, "ir": 2, "is": 1/2}).x
    p_sp = optimize.minimize(f, x0,
                       bounds=lu).x
    print("Nelder Mead Nosso", p_nm)
    print("Nelder Mead Scipy", p_sp)
    print("==============")

for function in functions:
    test_function(function, (10, 10), [(-100, 100), (-100, 100)])
