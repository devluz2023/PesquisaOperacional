import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


def resolver_esportes_radicais():
    # Max Z = 60*x1 + 40*x2  <=>  Min -60*x1 - 40*x2
    c = [-60.0, -40.0]

    # Matriz das restrições (A_ub @ x <= b_ub)
    A_ub = [
        [10.0, 10.0],  # Linha 1: 10*x1 + 10*x2 <= 100
        [3.0, 7.0],  # Linha 2:  3*x1 +  7*x2 <= 42
    ]
    b_ub = [100.0, 42.0]

    bounds = [(0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    return {
        "x1": float(res.x[0]),
        "x2": float(res.x[1]),
        "lucro_max": float(-res.fun),
    }


def plotar_grafico(solucao):
    x1_opt = solucao["x1"]
    x2_opt = solucao["x2"]
    z_opt = solucao["lucro_max"]

    x1_vals = np.linspace(0, 16, 800)
    x2_vals = np.linspace(0, 12, 800)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Fronteiras isolando x2:
    # Linha 1: 10x1 + 10x2 = 100 => x2 = 10 - x1
    r_linha1 = 10.0 - x1_vals
    # Linha 2: 3x1 + 7x2 = 42    => x2 = (42 - 3x1)/7
    r_linha2 = (42.0 - 3.0 * x1_vals) / 7.0

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(
        x1_vals,
        np.maximum(0, r_linha1),
        label=r"Linha 1: $10x_1 + 10x_2 \leq 100$",
        color="royalblue",
        linewidth=2,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_linha2),
        label=r"Linha 2: $3x_1 + 7x_2 \leq 42$",
        color="darkorange",
        linewidth=2,
    )

    # Região factível
    factivel = (
        (10.0 * X1 + 10.0 * X2 <= 100.0)
        & (3.0 * X1 + 7.0 * X2 <= 42.0)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    ax.imshow(
        factivel.astype(int),
        extent=(0, 16, 0, 12),
        origin="lower",
        cmap="Blues",
        alpha=0.25,
    )

    # Retas de Isolucro: 60x1 + 40x2 = Z => x2 = -1.5*x1 + Z/40
    ax.plot(
        x1_vals,
        -1.5 * x1_vals + 300.0 / 40.0,
        "crimson",
        linestyle=":",
        alpha=0.6,
        label=r"F.O. $Z = \text{R\$\,300}$",
    )
    ax.plot(
        x1_vals,
        -1.5 * x1_vals + 540.0 / 40.0,
        "crimson",
        linestyle="--",
        alpha=0.6,
        label=r"F.O. $Z = \text{R\$\,540}$ (Interseção)",
    )
    ax.plot(
        x1_vals,
        -1.5 * x1_vals + z_opt / 40.0,
        "crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima $Z^* = \text{{R\$\,}}{z_opt:.0f}$",
    )

    # Vértices da região factível
    ax.plot(0, 0, "ko", markersize=5)
    ax.plot(0, 6, "ko", markersize=6, label=r"$(0;\, 6)$ [$Z=240$]")
    ax.plot(7, 3, "ko", markersize=6, label=r"$(7;\, 3)$ [$Z=540$]")

    # Ponto ótimo
    ax.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=9,
        label=rf"Ótimo $({x1_opt:.0f};\, {x2_opt:.0f})$ [$Z^*={z_opt:.0f}$]",
    )

    # Vetor gradiente (direção de crescimento de Z)
    ax.annotate(
        "Sentido de Crescimento de Z",
        xy=(10, 0),
        xytext=(11, 4),
        arrowprops=dict(
            facecolor="crimson", shrink=0.08, width=1.5, headwidth=8
        ),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 11)
    ax.set_xlabel(r"Paraquedas ($x_1$)", fontsize=12)
    ax.set_ylabel(r"Asas-delta ($x_2$)", fontsize=12)
    ax.set_title(
        "Esportes Radicais S.A. — Maximização de Lucro", fontsize=14, pad=15
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sol = resolver_esportes_radicais()
    print("=" * 45)
    print("   ESPORTES RADICAIS S.A. — OTIMIZAÇÃO   ")
    print("=" * 45)
    print(f"Paraquedas a produzir (x1*) : {sol['x1']:.0f} unidades/semana")
    print(f"Asas-delta a produzir (x2*) : {sol['x2']:.0f} unidades/semana")
    print(f"Lucro Máximo Semanal (Z*)   : R$ {sol['lucro_max']:,.2f}")
    print("=" * 45)

    plotar_grafico(sol)