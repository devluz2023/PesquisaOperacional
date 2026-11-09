"""
Otimização da Produção de Camisas (Pequena Malharia)
Resolução exata via SciPy (HiGHS) e plotagem gráfica da região viável.

Problema:
    Max Z = 2*x1 + 3*x2
    sujeito a:
        3.0*x1 + 3.0*x2 <= 210   (Corte)
        1.5*x1 + 3.0*x2 <= 180   (Costura)
        5.0*x1 + 3.0*x2 <= 330   (Acabamento)
        x1, x2 >= 0
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


def resolver_malharia():
    # linprog minimiza: Max Z <=> Min -Z
    c = [-2.0, -3.0]

    A_ub = [
        [3.0, 3.0],  # Corte
        [1.5, 3.0],  # Costura
        [5.0, 3.0],  # Acabamento
    ]
    b_ub = [210.0, 180.0, 330.0]

    bounds = [(0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"Erro na resolução: {res.message}")

    return {
        "manga_curta": float(res.x[0]),
        "manga_comprida": float(res.x[1]),
        "lucro_max": float(-res.fun),
        "folga_corte": float(res.slack[0]),
        "folga_costura": float(res.slack[1]),
        "folga_acabamento": float(res.slack[2]),
    }


def plotar_grafico(solucao):
    x1_opt = solucao["manga_curta"]
    x2_opt = solucao["manga_comprida"]
    z_opt = solucao["lucro_max"]

    # Malha de pontos
    x1_vals = np.linspace(0, 85, 1000)
    x2_vals = np.linspace(0, 75, 1000)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Fronteiras isolando x2:
    # Corte: 3x1 + 3x2 = 210 => x2 = 70 - x1
    r_corte = 70.0 - x1_vals

    # Costura: 1.5x1 + 3x2 = 180 => x2 = (180 - 1.5x1)/3 = 60 - 0.5x1
    r_costura = (180.0 - 1.5 * x1_vals) / 3.0

    # Acabamento: 5x1 + 3x2 = 330 => x2 = (330 - 5x1)/3 = 110 - (5/3)x1
    r_acabamento = (330.0 - 5.0 * x1_vals) / 3.0

    fig, ax = plt.subplots(figsize=(11, 7.5))

    # Retas de restrição
    ax.plot(
        x1_vals,
        np.maximum(0, r_corte),
        label=r"Corte: $3x_1 + 3x_2 \leq 210$ (Ativa)",
        color="royalblue",
        linewidth=2.2,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_costura),
        label=r"Costura: $1{,}5x_1 + 3x_2 \leq 180$ (Ativa)",
        color="darkorange",
        linewidth=2.2,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_acabamento),
        label=r"Acabamento: $5x_1 + 3x_2 \leq 330$ (Folga: 80h)",
        color="forestgreen",
        linewidth=2,
    )

    # Região factível
    regiao_factivel = (
        (3.0 * X1 + 3.0 * X2 <= 210.0)
        & (1.5 * X1 + 3.0 * X2 <= 180.0)
        & (5.0 * X1 + 3.0 * X2 <= 330.0)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    ax.imshow(
        regiao_factivel.astype(int),
        extent=(0, 85, 0, 75),
        origin="lower",
        cmap="Greens",
        alpha=0.25,
    )

    # Retas da Função-Objetivo (Isolucro: 2x1 + 3x2 = Z => x2 = - (2/3)x1 + Z/3)
    z_sub = 140.0
    ax.plot(
        x1_vals,
        -(2.0 / 3.0) * x1_vals + z_sub / 3.0,
        color="crimson",
        linestyle=":",
        alpha=0.6,
        label=rf"F.O. Sub-ótima ($Z = \text{{R\$\,}}{z_sub:.0f}$)",
    )
    ax.plot(
        x1_vals,
        -(2.0 / 3.0) * x1_vals + z_opt / 3.0,
        color="crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima ($Z^* = \text{{R\$\,}}{z_opt:.0f}$)",
    )

    # Vértices (Pontos Extremos)
    pontos_extremos = {
        r"$V_1(0;\, 0)$": (0, 0),
        r"$V_2(0;\, 60)$": (0, 60),
        r"$V_4(60;\, 10)$": (60, 10),
        r"$V_5(66;\, 0)$": (66, 0),
    }

    for rotulo, (vx, vy) in pontos_extremos.items():
        z_v = 2 * vx + 3 * vy
        ax.plot(vx, vy, "ko", markersize=5)
        ax.annotate(
            f"{rotulo}\n[Z = R$ {z_v:.0f}]",
            (vx, vy),
            textcoords="offset points",
            xytext=(8, 5),
            fontsize=9,
        )

    # Destaque do Ponto Ótimo
    ax.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=10,
        label=rf"Ótimo $V_3({x1_opt:.0f};\, {x2_opt:.0f})$ [$Z^*=\text{{R\$\,}}{z_opt:.0f}$]",
    )
    ax.annotate(
        f"$V_3(20;\, 50)$ - ÓTIMO\n[Z* = R$ {z_opt:.0f}]",
        (x1_opt, x2_opt),
        textcoords="offset points",
        xytext=(10, 10),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    # Vetor indicando a direção do gradiente da função-objetivo
    ax.annotate(
        "Sentido de Maximização (Crescimento de Z)",
        xy=(x1_opt, x2_opt),
        xytext=(x1_opt + 10, x2_opt + 12),
        arrowprops=dict(
            facecolor="crimson", shrink=0.08, width=1.5, headwidth=8
        ),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    ax.set_xlim(0, 80)
    ax.set_ylim(0, 72)
    ax.set_xlabel(r"Camisas Manga Curta ($x_1$)", fontsize=12)
    ax.set_ylabel(r"Camisas Manga Comprida ($x_2$)", fontsize=12)
    ax.set_title(
        r"Pequena Malharia — Maximização do Lucro ($\max Z = 2x_1 + 3x_2$)",
        fontsize=13,
        pad=15,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sol = resolver_malharia()
    print("=" * 52)
    print("      PEQUENA MALHARIA — PLANO SEMANAL ÓTIMO        ")
    print("=" * 52)
    print(f"Camisas Manga Curta   (x1*) : {sol['manga_curta']:.0f} unidades")
    print(f"Camisas Manga Comprida(x2*) : {sol['manga_comprida']:.0f} unidades")
    print("-" * 52)
    print(f"Lucro Máximo Semanal  (Z*)  : R$ {sol['lucro_max']:,.2f}")
    print("=" * 52)
    print("               DIAGNÓSTICO DE RECURSOS              ")
    print("-" * 52)
    print(f"Folga no Corte              : {sol['folga_corte']:.1f} h (Esgotado)")
    print(f"Folga na Costura            : {sol['folga_costura']:.1f} h (Esgotado)")
    print(f"Folga no Acabamento         : {sol['folga_acabamento']:.1f} h (Sobra)")
    print("=" * 52)

    plotar_grafico(sol)