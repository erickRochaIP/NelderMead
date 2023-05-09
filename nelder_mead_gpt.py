import numpy as np

def nelder_mead(f, x0, step=1.0, max_iter=1000, tol=1e-6):
    '''
    f: função objetivo que deve ser minimizada.
    x0: vetor inicial de dimensão n.
    step: tamanho do passo para gerar os pontos simplex.
    max_iter: número máximo de iterações.
    tol: tolerância para o critério de parada.
    '''
    n = len(x0)
    simplex = np.zeros((n+1, n))
    simplex[0] = x0
    for i in range(n):
        point = np.array(x0)
        point[i] = x0[i] + step
        simplex[i+1] = point
    fx = np.zeros(n+1)
    for i in range(n+1):
        fx[i] = f(simplex[i])
    for i in range(max_iter):
        order = np.argsort(fx)
        simplex = simplex[order]
        fx = fx[order]
        x0 = np.mean(simplex[:-1], axis=0)
        xr = x0 + (x0 - simplex[-1])
        fxr = f(xr)
        if fxr < fx[0]:
            xe = x0 + 2 * (xr - x0)
            fxe = f(xe)
            if fxe < fxr:
                simplex[-1] = xe
                fx[-1] = fxe
            else:
                simplex[-1] = xr
                fx[-1] = fxr
        else:
            if fxr < fx[-2]:
                simplex[-1] = xr
                fx[-1] = fxr
            xc = x0 + 0.5 * (simplex[-1] - x0)
            fxc = f(xc)
            if fxc < fx[-1]:
                simplex[-1] = xc
                fx[-1] = fxc
            else:
                for j in range(1, n+1):
                    simplex[j] = 0.5 * (simplex[0] + simplex[j])
                    fx[j] = f(simplex[j])
        if np.max(np.abs(simplex - simplex[0])) < tol and np.max(np.abs(fx - fx[0])) < tol:
            break
    return simplex[0], fx[0], i+1
