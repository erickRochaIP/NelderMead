from scipy import optimize

import benchmark_functions as bf
from nelder_mead import nelder_mead, _minimize_neldermead

def string_point(x):
    s = "("
    for xi in x[:-1]:
        s += f"{xi:.3f}, "
    s += f"{x[-1]:.3f})"
    return s

def test_function(f, x0, lu):
    if f.__name__ is not None:
        print(f.__name__)
        print()
    
    p_nm = nelder_mead(f, x0, 10,
                 lu,
                 params = {"ie": 2, "ic": 1/2, "ir": 2, "is": 1/2},
                 eps_x=1e-6).x
    # p_sp = optimize.minimize(f, x0,
    #                   bounds=lu).x
    #p_csp = _minimize_neldermead(f, x0, bounds=lu, maxiter=500)
    
    print(f"Nelder Mead Nosso: x*={string_point(p_nm)}; f(x*)={f(p_nm):.3f}")
    # print(f"Nelder Mead Scipy: x*={string_point(p_sp)}; f(x*)={f(p_sp):.3f}")
    # print(f"Nelder Mead Scipy Copiado: x*={string_point(p_csp)}; f(x*)={f(p_csp):.3f}")
    print("==============")


functions = [
    bf.zakharov_function,
    # bf.rosenbrock_function,
    # bf.expanded_schaffer_function,
    # bf.rastrigin_function,
    # bf.levy_function
    ]

x0 = [50]
lu = [(-10, 10)]

for function in functions:
    test_function(function, x0 * 2, lu * 2)
    test_function(function, x0 * 10, lu * 10)
