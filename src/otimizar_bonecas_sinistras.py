"""
Otimização da Produção de Bonecas (Bonecas Sinistras S.A.)
Determinação de pontos extremos, infinitas soluções ótimas e plotagem gráfica.

Problema:
    Max Z = 2*x1 + 1*x2
    sujeito a:
        450 <= 6*x1 + 3*x2 <= 480   (Montador 1)
        450 <= 2*x1 + 4*x2 <= 480   (Montador 2)
        -30 <= 4*x1 - x2 <= 30      (Balanceamento: |T1 - T2| <= 30)
        x1, x2 >= 0
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


def resolver_bonecas():
    # linprog minimiza: Max Z <=> Min -Z
    c = [-2.0, -1.0]

    A_ub = [
        [6.0, 3.0],    # T1 <= 480
        [-6.0, -3.0],  # T1 >= 450
        [2.0, 4.0],    # T2 <= 480
        [-2.0, -4.0],  # T2 >= 450
        [4.0, -1.0],   # T1 - T2 <= 30
        [-4.0, 1.0],   # T2 - T1 <= 30
    ]
    b_ub = [480.0, -450.0, 480.0, -450.0, 30.0, 30.0]

    bounds = [(0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"Erro na resolução: {res.message}")

    return {
        "x1": float(res.x[0]),
        "x2": float(res.x[1]),
        "lucro_max": float(-res.fun),
    }


def plotar_grafico():
    x1_vals = np.linspace(10, 45, 1000)
    x2_vals = np.linspace(80, 125, 1000)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Fronteiras isolando x2:
    # Montador 1:
    r_t1_max = (480.0 - 6.0 * x1_vals) / 3.0  # 160 - 2*x1
    r_t1_min = (450.0 - 6.0 * x1_vals) / 3.0  # 150 - 2*x1

    # Montador 2:
    r_t2_max = (480.0 - 2.0 * x1_vals) / 4.0  # 120 - 0.5*x1
    r_t2_min = (450.0 - 2.0 * x1_vals) / 4.0  # 112.5 - 0.5*x1

    # Balanceamento:
    r_bal1 = 4.0 * x1_vals - 30.0  # T1 - T2 <= 30 => x2 >= 4x1 - 30
    r_bal2 = 4.0 * x1_vals + 30.0  # T2 - T1 <= 30 => x2 <= 4x1 + 30

    fig, ax = plt.subplots(figsize=(11, 7.5))

    # Plot das fronteiras
    ax.plot(
        x1_vals,
        r_t1_max,
        label=r"Montador 1 Máx (480 min): $2x_1 + x_2 = 160$",
        color="royalblue",
        linewidth=2.2,
    )
    ax.plot(
        x1_vals,
        r_t1_min,
        label=r"Montador 1 Mín (450 min): $2x_1 + x_2 = 150$",
        color="royalblue",
        linestyle="--",
        linewidth=1.8,
    )
    ax.plot(
        x1_vals,
        r_t2_max,
        label=r"Montador 2 Máx (480 min): $x_1 + 2x_2 = 240$",
        color="darkorange",
        linewidth=2.2,
    )
    ax.plot(
        x1_vals,
        r_t2_min,
        label=r"Montador 2 Mín (450 min): $x_1 + 2x_2 = 225$",
        color="darkorange",
        linestyle="--",
        linewidth=1.8,
    )
    ax.plot(
        x1_vals,
        r_bal1,
        label=r"Balanceamento: $4x_1 - x_2 \leq 30$",
        color="purple",
        linestyle=":",
        linewidth=1.5,
    )
    ax.plot(
        x1_vals,
        r_bal2,
        label=r"Balanceamento: $-4x_1 + x_2 \leq 30$",
        color="purple",
        linestyle=":",
        linewidth=1.5,
    )

    # Região factível conjunta
    T1 = 6.0 * X1 + 3.0 * X2
    T2 = 2.0 * X1 + 4.0 * X2
    regiao = (
        (T1 <= 480.0)
        & (T1 >= 450.0)
        & (T2 <= 480.0)
        & (T2 >= 450.0)
        & (T1 - T2 <= 30.0)
        & (T2 - T1 <= 30.0)
    )

    ax.imshow(
        regiao.astype(int),
        extent=(10, 45, 80, 125),
        origin="lower",
        cmap="Greens",
        alpha=0.25,
    )

    # Segmento de infinitas soluções ótimas (entre A e B)
    x1_otimo_seg = np.linspace(80 / 3, 95 / 3, 100)
    x2_otimo_seg = 160.0 - 2.0 * x1_otimo_seg
    ax.plot(
        x1_otimo_seg,
        x2_otimo_seg,
        color="crimson",
        linewidth=4.5,
        label=r"Segmento de Soluções Ótimas ($Z^* = \text{R\$\,160,00}$)",
        zorder=5,
    )

    # Vértices (Pontos Extremos)
    vertices = {
        r"$A\left(\frac{80}{3};\, \frac{320}{3}\right)$": (
            80 / 3,
            320 / 3,
            "Z = R$ 160",
        ),
        r"$B\left(\frac{95}{3};\, \frac{290}{3}\right)$": (
            95 / 3,
            290 / 3,
            "Z = R$ 160",
        ),
        r"$C(20;\, 110)$": (20.0, 110.0, "Z = R$ 150"),
        r"$D(25;\, 100)$": (25.0, 100.0, "Z = R$ 150"),
    }

    for rotulo, (vx, vy, z_str) in vertices.items():
        ax.plot(vx, vy, "ro" if "160" in z_str else "ko", markersize=8)
        ax.annotate(
            f"{rotulo}\n[{z_str}]",
            (vx, vy),
            textcoords="offset points",
            xytext=(-15, 12) if vy > 105 else (10, -15),
            fontsize=9,
            fontweight="bold" if "160" in z_str else "normal",
        )

    # Destaque de uma solução inteira viável ótima (30, 100)
    ax.plot(
        30,
        100,
        "m*",
        markersize=13,
        label=r"Solução Inteira Ótima $(30;\, 100)$ [$Z^*=\text{R\$\,160}$]",
        zorder=6,
    )

    ax.set_xlim(15, 40)
    ax.set_ylim(85, 120)
    ax.set_xlabel(r"Vampiresca ($x_1$)", fontsize=12)
    ax.set_ylabel(r"Lobimulher ($x_2$)", fontsize=12)
    ax.set_title(
        r"Bonecas Sinistras S.A. — Otimização com Soluções Múltiplas ($\max Z = 2x_1 + x_2$)",
        fontsize=13,
        pad=15,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=8.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sol = resolver_bonecas()
    print("=" * 55)
    print("     BONECAS SINISTRAS S.A. — PLANO DIÁRIO ÓTIMO     ")
    print("=" * 55)
    print(f"Lucro Máximo Diário (Z*) : R$ {sol['lucro_max']:,.2f}")
    print("-" * 55)
    print("O problema possui INFINITAS SOLUÇÕES ÓTIMAS ao longo do")
    print("segmento conectando os vértices A e B:")
    print("  • Vértice A: (26,67 Vampiresca; 106,67 Lobimulher)")
    print("    -> T1 = 480 min (8h00) | T2 = 480 min (8h00)")
    print("  • Vértice B: (31,67 Vampiresca; 96,67 Lobimulher)")
    print("    -> T1 = 480 min (8h00) | T2 = 450 min (7h30)")
    print("-" * 55)
    print("Solução Inteira Recomendada:")
    print("  • Vampiresca (x1*) : 30 unidades")
    print("  • Lobimulher (x2*) : 100 unidades")
    print("  • Tempo Montador 1 : 480 min (8 horas exatas)")
    print("  • Tempo Montador 2 : 460 min (7 horas e 40 minutos)")
    print("=" * 55)

    plotar_grafico()