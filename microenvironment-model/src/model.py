"""
Core utilities for the two-field tumor microenvironment model and analysis.
Equations (dimensionless, linearized around phi=0, rho=0):
    ∂t phi = K ∇^2 phi - a phi - b phi^3 - gamma rho
    ∂t rho = D_rho ∇^2 rho - c rho - gamma phi
Default parameters: K=b=c=1.0; D_rho=0.6.
"""
import numpy as np

def laplacian(u):
    return (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
            np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4.0*u)

def simulate_phi_rho(N=96, steps=400, dt=0.02, seed=0,
                     a=-0.4, b=1.0, c=1.0, gamma=1.0, K=1.0, D_rho=0.6):
    rng = np.random.default_rng(seed)
    phi = 0.03 * rng.standard_normal((N, N))
    rho = 0.03 * rng.standard_normal((N, N))
    checkpoints = [0, steps//4, steps//2, steps-1]
    snaps = {}
    for t in range(steps):
        phi3 = phi*phi*phi
        lap_phi = laplacian(phi)
        lap_rho = laplacian(rho)
        dphi = K*lap_phi - a*phi - b*phi3 - gamma*rho
        drho = D_rho*lap_rho - c*rho - gamma*phi
        phi += dt*dphi
        rho += dt*drho
        phi = np.clip(phi, -5.0, 5.0)
        rho = np.clip(rho, -5.0, 5.0)
        if t in checkpoints:
            snaps[t] = phi.copy()
    return snaps, phi, rho

def dispersion_relation(k, a=-0.4, c=1.0, gamma=1.0, K=1.0, D_rho=0.6):
    M11 = -a - K*(k*k)
    M22 = -c - D_rho*(k*k)
    Tr = M11 + M22
    Det = M11*M22 - (gamma*gamma)
    disc = Tr*Tr - 4.0*Det
    sqrt_disc = np.sqrt(np.maximum(disc, 0.0))
    lam_plus = 0.5*(Tr + sqrt_disc)
    lam_minus = 0.5*(Tr - sqrt_disc)
    return lam_plus, lam_minus

def max_growth_rate_over_k(a, gamma, c=1.0, K=1.0, D_rho=0.6, k_max=2.5, nk=256):
    ks = np.linspace(0.0, k_max, nk)
    lam_plus, _ = dispersion_relation(ks, a=a, c=c, gamma=gamma, K=K, D_rho=D_rho)
    lam_plus = np.real(lam_plus)
    idx = int(np.argmax(lam_plus))
    return lam_plus[idx], ks[idx], ks, lam_plus

def radial_structure_factor(field):
    f = np.fft.fftn(field)
    P = np.abs(f)**2
    N = field.shape[0]
    kx = np.fft.fftfreq(N)*N
    ky = np.fft.fftfreq(N)*N
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    KR = np.sqrt(KX**2 + KY**2)
    kmax = int(KR.max())
    S = np.zeros(kmax+1)
    count = np.zeros(kmax+1)
    for i in range(N):
        for j in range(N):
            kbin = int(round(KR[i, j]))
            if kbin <= kmax:
                S[kbin] += P[i, j]
                count[kbin] += 1
    count[count == 0] = 1.0
    S /= count
    kbins = np.arange(kmax+1)
    return kbins, S

def front_roughness(binary_field):
    H, W = binary_field.shape
    heights = np.full(W, np.nan)
    for x in range(W):
        ys = np.where(binary_field[:, x] > 0.5)[0]
        if ys.size > 0:
            heights[x] = ys.max()
    valid = ~np.isnan(heights)
    if valid.sum() < 2:
        return np.nan
    return np.std(heights[valid])
