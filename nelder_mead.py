import numpy as np

from simplex import Simplex, PontoAvaliacao

def prints(str):
    if True:
        print(str)

# Recebe uma funcao, ponto inicial, quantidade de iteracoes, limites, parametros e tolerancia
# Retorna o ponto cujo valor da funcao e o menor encontrado
def nelder_mead(f, x0, avals_usr, lu, params = None, eps_x = 0.0):
    if params is None:
        params = {}
    coef_reflexao = params["ir"] if "ir" in params else 2
    coef_exp = params["ie"] if "ie" in params else 2
    coef_contracao = params["ic"] if "ic" in params else 1/2
    coef_encolhimento = params["is"] if "is" in params else 1/2
    
    k = 0

    S = Simplex(f, x0, lu)
    pior, segundo_pior, melhor = S.extrair_dados()
    
    melhor_dos_melhores = melhor
    atual_melhor = melhor

    PontoAvaliacao.reset_avals()
    while avals_usr > PontoAvaliacao.avals:
        print(PontoAvaliacao.avals)
        if S.estagnou(eps_x):
            prints("estagnou")
            if atual_melhor == melhor:
                k +=1
            else:
                k = 0
            melhor_dos_melhores = min(melhor_dos_melhores, atual_melhor, melhor)
            atual_melhor = melhor
            S = Simplex(f, atual_melhor.x, lu, k)
            pior, segundo_pior, melhor = S.extrair_dados()
            continue

        centroide = S.calcular_centroide()
        refletido = PontoAvaliacao.calcular_ponto_deslocado(pior.x, centroide, coef_reflexao)
        refletido = PontoAvaliacao(refletido, f, lu)
        if segundo_pior > refletido >= melhor:
            prints("refletido")
            S.substituir_pior_ponto(refletido)
            pior, segundo_pior, melhor = S.extrair_dados()
            continue
        if melhor > refletido:
            expandido = PontoAvaliacao.calcular_ponto_deslocado(centroide, refletido.x, coef_exp)
            expandido = PontoAvaliacao(expandido, f, lu)
            if refletido > expandido:
                prints("expandido")
                S.substituir_pior_ponto(expandido)
            else:
                prints("refletido")
                S.substituir_pior_ponto(refletido)
            pior, segundo_pior, melhor = S.extrair_dados()
            continue
        if pior >= refletido:
            contraido_externo = PontoAvaliacao.calcular_ponto_deslocado(centroide, refletido.x, coef_contracao)
            contraido_externo = PontoAvaliacao(contraido_externo, f, lu)
            if refletido > contraido_externo:
                prints("contraido externo")
                S.substituir_pior_ponto(contraido_externo)
                pior, segundo_pior, melhor = S.extrair_dados()
                continue
        else:
            contraido_interno = PontoAvaliacao.calcular_ponto_deslocado(centroide, refletido.x, -coef_contracao)
            contraido_interno = PontoAvaliacao(contraido_interno, f, lu)
            if pior > contraido_interno:
                prints("contraido interno")
                S.substituir_pior_ponto(contraido_interno)
                pior, segundo_pior, melhor = S.extrair_dados()
                continue

        prints("simplex encolhido")
        S.contrair_simplex(coef_encolhimento, f, lu)
        pior, segundo_pior, melhor = S.extrair_dados()

    return min(melhor_dos_melhores, atual_melhor, melhor)



# Implementacao neldermead scipy
def _minimize_neldermead(func, x0, args=(), callback=None,
                         maxiter=None, maxfev=None, disp=False,
                         return_all=False, initial_simplex=None,
                         xatol=1e-4, fatol=1e-4, adaptive=False, bounds=None,
                         **unknown_options):
    """
    Minimization of scalar function of one or more variables using the
    Nelder-Mead algorithm.

    Options
    -------
    disp : bool
        Set to True to print convergence messages.
    maxiter, maxfev : int
        Maximum allowed number of iterations and function evaluations.
        Will default to ``N*200``, where ``N`` is the number of
        variables, if neither `maxiter` or `maxfev` is set. If both
        `maxiter` and `maxfev` are set, minimization will stop at the
        first reached.
    return_all : bool, optional
        Set to True to return a list of the best solution at each of the
        iterations.
    initial_simplex : array_like of shape (N + 1, N)
        Initial simplex. If given, overrides `x0`.
        ``initial_simplex[j,:]`` should contain the coordinates of
        the jth vertex of the ``N+1`` vertices in the simplex, where
        ``N`` is the dimension.
    xatol : float, optional
        Absolute error in xopt between iterations that is acceptable for
        convergence.
    fatol : number, optional
        Absolute error in func(xopt) between iterations that is acceptable for
        convergence.
    adaptive : bool, optional
        Adapt algorithm parameters to dimensionality of problem. Useful for
        high-dimensional minimization [1]_.
    bounds : sequence or `Bounds`, optional
        Bounds on variables. There are two ways to specify the bounds:

            1. Instance of `Bounds` class.
            2. Sequence of ``(min, max)`` pairs for each element in `x`. None
               is used to specify no bound.

        Note that this just clips all vertices in simplex based on
        the bounds.

    References
    ----------
    .. [1] Gao, F. and Han, L.
       Implementing the Nelder-Mead simplex algorithm with adaptive
       parameters. 2012. Computational Optimization and Applications.
       51:1, pp. 259-277

    """
    maxfun = maxfev
    retall = return_all

    x0 = np.asfarray(x0).flatten()

    if adaptive:
        dim = float(len(x0))
        rho = 1
        chi = 1 + 2/dim
        psi = 0.75 - 1/(2*dim)
        sigma = 1 - 1/dim
    else:
        rho = 1
        chi = 2
        psi = 0.5
        sigma = 0.5

    nonzdelt = 0.05
    zdelt = 0.00025

    if bounds is not None:
        lower_bound, upper_bound = [b[0] for b in bounds], [b[1] for b in bounds]

    if bounds is not None:
        x0 = np.clip(x0, lower_bound, upper_bound)

    if initial_simplex is None:
        N = len(x0)

        sim = np.empty((N + 1, N), dtype=x0.dtype)
        sim[0] = x0
        for k in range(N):
            y = np.array(x0, copy=True)
            if y[k] != 0:
                y[k] = (1 + nonzdelt)*y[k]
            else:
                y[k] = zdelt
            sim[k + 1] = y
    else:
        sim = np.asfarray(initial_simplex).copy()
        if sim.ndim != 2 or sim.shape[0] != sim.shape[1] + 1:
            raise ValueError("`initial_simplex` should be an array of shape (N+1,N)")
        if len(x0) != sim.shape[1]:
            raise ValueError("Size of `initial_simplex` is not consistent with `x0`")
        N = sim.shape[1]

    if retall:
        allvecs = [sim[0]]

    # If neither are set, then set both to default
    if maxiter is None and maxfun is None:
        maxiter = N * 200
        maxfun = N * 200
    elif maxiter is None:
        # Convert remaining Nones, to np.inf, unless the other is np.inf, in
        # which case use the default to avoid unbounded iteration
        if maxfun == np.inf:
            maxiter = N * 200
        else:
            maxiter = np.inf
    elif maxfun is None:
        if maxiter == np.inf:
            maxfun = N * 200
        else:
            maxfun = np.inf

    if bounds is not None:
        sim = np.clip(sim, lower_bound, upper_bound)

    one2np1 = list(range(1, N + 1))
    fsim = np.full((N + 1,), np.inf, dtype=float)

    # fcalls, func = _wrap_scalar_function_maxfun_validation(func, args, maxfun)

    try:
        for k in range(N + 1):
            fsim[k] = func(sim[k])
    except:
        pass
    finally:
        ind = np.argsort(fsim)
        sim = np.take(sim, ind, 0)
        fsim = np.take(fsim, ind, 0)

    ind = np.argsort(fsim)
    fsim = np.take(fsim, ind, 0)
    # sort so sim[0,:] has the lowest function value
    sim = np.take(sim, ind, 0)

    iterations = 1

    while (iterations < maxiter):
        try:
            if (np.max(np.ravel(np.abs(sim[1:] - sim[0]))) <= xatol and
                    np.max(np.abs(fsim[0] - fsim[1:])) <= fatol):
                break

            xbar = np.add.reduce(sim[:-1], 0) / N
            xr = (1 + rho) * xbar - rho * sim[-1]
            if bounds is not None:
                xr = np.clip(xr, lower_bound, upper_bound)
            fxr = func(xr)
            doshrink = 0

            if fxr < fsim[0]:
                xe = (1 + rho * chi) * xbar - rho * chi * sim[-1]
                if bounds is not None:
                    xe = np.clip(xe, lower_bound, upper_bound)
                fxe = func(xe)

                if fxe < fxr:
                    prints("expandido")
                    sim[-1] = xe
                    fsim[-1] = fxe
                else:
                    prints("refletido")
                    sim[-1] = xr
                    fsim[-1] = fxr
            else:  # fsim[0] <= fxr
                if fxr < fsim[-2]:
                    prints("refletido")
                    sim[-1] = xr
                    fsim[-1] = fxr
                else:  # fxr >= fsim[-2]
                    # Perform contraction
                    if fxr < fsim[-1]:
                        xc = (1 + psi * rho) * xbar - psi * rho * sim[-1]
                        if bounds is not None:
                            xc = np.clip(xc, lower_bound, upper_bound)
                        fxc = func(xc)

                        if fxc <= fxr:
                            prints("contraido externo")
                            sim[-1] = xc
                            fsim[-1] = fxc
                        else:
                            doshrink = 1
                    else:
                        # Perform an inside contraction
                        xcc = (1 - psi) * xbar + psi * sim[-1]
                        if bounds is not None:
                            xcc = np.clip(xcc, lower_bound, upper_bound)
                        fxcc = func(xcc)

                        if fxcc < fsim[-1]:
                            prints("contraido interno")
                            sim[-1] = xcc
                            fsim[-1] = fxcc
                        else:
                            doshrink = 1

                    if doshrink:
                        prints("encolhido")
                        for j in one2np1:
                            sim[j] = sim[0] + sigma * (sim[j] - sim[0])
                            if bounds is not None:
                                sim[j] = np.clip(
                                    sim[j], lower_bound, upper_bound)
                            fsim[j] = func(sim[j])
            iterations += 1
        except:
            pass
        finally:
            ind = np.argsort(fsim)
            sim = np.take(sim, ind, 0)
            fsim = np.take(fsim, ind, 0)
            if callback is not None:
                callback(sim[0])
            if retall:
                allvecs.append(sim[0])

    x = sim[0]
    fval = np.min(fsim)
    
    return x

