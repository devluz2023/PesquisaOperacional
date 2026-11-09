"""
Otimização da Bebida Energética (Have Fun S.A.)
Minimização de custo por lata via SciPy (HiGHS) e plotagem gráfica.

Problema:
    Min Z = 0.06*x1 + 0.08*x2
    sujeito a:
        8*x1 + 6*x2 >= 48   (Extrato de Guaraná mín.)
        1*x1 + 2*x2 >= 12   (Cafeína mín.)
        1*x1 + 2*x2 <= 20   (Cafeína máx.)
        x1, x2 >= 0
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


def resolver_energetico():
    # Coeficientes de custo (Minimização padrão no linprog)
    c = [0.06, 0.08]

    # Convertendo as restrições (>=) para (<=) multiplicando por -1
    A_ub = [
        [-8.0, -6.0],  # -8x1 - 6x2 <= -48  (Guaraná mín.)
        [-1.0, -2.0],  # -1x1 - 2x2 <= -12  (Cafeína mín.)
        [1.0, 2.0],  #  1x1 + 2x2 <=  20  (Cafeína máx.)
    ]
    b_ub = [-48.0, -12.0, 20.0]

    bounds = [(0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"Falha na convergência do solver: {res.message}")

    return {
        "x1": float(res.x[0]),
        "x2": float(res.x[1]),
        "custo_min": float(res.fun),
    }


def plotar_grafico(solucao):
    x1_opt = solucao["x1"]
    x2_opt = solucao["x2"]
    z_opt = solucao["custo_min"]

    # Malha para o plano cartesiano
    x1_vals = np.linspace(0, 24, 1000)
    x2_vals = np.linspace(0, 14, 1000)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Fronteiras isolando x2:
    # R1: 8x1 + 6x2 = 48  => x2 = (48 - 8x1)/6 = 8 - (4/3)x1
    r_guarana = (48.0 - 8.0 * x1_vals) / 6.0

    # R2: x1 + 2x2 = 12   => x2 = (12 - x1)/2 = 6 - 0.5x1
    r_caf_min = (12.0 - x1_vals) / 2.0

    # R3: x1 + 2x2 = 20   => x2 = (20 - x1)/2 = 10 - 0.5x1
    r_caf_max = (20.0 - x1_vals) / 2.0

    fig, ax = plt.subplots(figsize=(11, 7))

    # Curvas de restrição
    ax.plot(
        x1_vals,
        np.maximum(0, r_guarana),
        label=r"Guaraná Mín.: $8x_1 + 6x_2 \geq 48$",
        color="royalblue",
        linewidth=2,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_caf_min),
        label=r"Cafeína Mín.: $x_1 + 2x_2 \geq 12$",
        color="darkorange",
        linewidth=2,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_caf_max),
        label=r"Cafeína Máx.: $x_1 + 2x_2 \leq 20$",
        color="forestgreen",
        linewidth=2,
        linestyle="-.",
    )

    # Região factível
    regiao_factivel = (
        (8.0 * X1 + 6.0 * X2 >= 48.0)
        & (1.0 * X1 + 2.0 * X2 >= 12.0)
        & (1.0 * X1 + 2.0 * X2 <= 20.0)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    ax.imshow(
        regiao_factivel.astype(int),
        extent=(0, 24, 0, 14),
        origin="lower",
        cmap="Blues",
        alpha=0.25,
    )

    # Retas da Função-Objetivo (Isocusto): 0.06x1 + 0.08x2 = Z => x2 = -0.75x1 + Z/0.08
    # 1. Reta com Z maior (sub-ótima)
    z_sub = 0.80
    ax.plot(
        x1_vals,
        -0.75 * x1_vals + z_sub / 0.08,
        color="crimson",
        linestyle="--",
        alpha=0.6,
        label=rf"F.O. $Z = \text{{R\$\,}}{z_sub:.2f}$ (Sub-ótima)",
    )

    # 2. Reta no ponto ótimo
    ax.plot(
        x1_vals,
        -0.75 * x1_vals + z_opt / 0.08,
        color="crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima $Z^* = \text{{R\$\,}}{z_opt:.3f}$",
    )

    # Vértices do pentágono factível
    vertices = {
        r"$E(0; 8)$": (0.0, 8.0),
        r"$D(0; 10)$": (0.0, 10.0),
        r"$B(12; 0)$": (12.0, 0.0),
        r"$C(20; 0)$": (20.0, 0.0),
    }
    for rotulo, (vx, vy) in vertices.items():
        ax.plot(vx, vy, "ko", markersize=5)
        ax.annotate(
            rotulo,
            (vx, vy),
            textcoords="offset points",
            xytext=(7, 5),
            fontsize=9,
        )

    # Vértice ótimo destacado
    ax.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=9,
        label=rf"Ótimo $A({x1_opt:.1f}; {x2_opt:.1f})$ [$Z^*={z_opt:.3f}$]",
    )

    # Vetor indicando a direção de minimização
    ax.annotate(
        "Sentido de Minimização (em direção à origem)",
        xy=(2.4, 4.8),
        xytext=(8.0, 8.5),
        arrowprops=dict(
            facecolor="crimson", shrink=0.08, width=1.5, headwidth=8
        ),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    ax.set_xlim(0, 22)
    ax.set_ylim(0, 12)
    ax.set_xlabel(r"Doses de Solução Red ($x_1$)", fontsize=12)
    ax.set_ylabel(r"Doses de Solução Blue ($x_2$)", fontsize=12)
    ax.set_title(
        r"Have Fun S.A. — Otimização da Composição do Energético ($\min Z = 0{,}06x_1 + 0{,}08x_2$)",
        fontsize=13,
        pad=15,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    resultado = resolver_energetico()
    print("=" * 45)
    print("      HAVE FUN S.A. — RESULTADO ÓTIMO        ")
    print("=" * 45)
    print(
        f"Doses Solução Red  (x1*) : {resultado['x1']:.2f} doses ({resultado['x1']*10:.1f} ml)"
    )
    print(
        f"Doses Solução Blue (x2*) : {resultado['x2']:.2f} doses ({resultado['x2']*10:.1f} ml)"
    )
    print(f"Custo Mínimo/Lata  (Z*)  : R$ {resultado['custo_min']:.4f}")
    print("=" * 45)

    plotar_grafico(resultado)