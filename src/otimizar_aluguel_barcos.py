"""
Otimização de Aluguel de Embarcações (Capitão Caverna S.A.)
Resolução exata e visualização geométrica tridimensional (R³).
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import linprog


def resolver_capitao_caverna():
    c = [-50.0, -70.0, -100.0]
    A_ub = [
        [1.0, 1.0, 1.0],  # Capitães <= 10
        [1.0, 2.0, 3.0],  # Tripulantes <= 18
    ]
    b_ub = [10.0, 18.0]
    bounds = [(0, 4), (0, 8), (0, 3)]
    integrality = [1, 1, 1]

    res = linprog(
        c,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=bounds,
        integrality=integrality,
        method="highs",
    )

    x1, x2, x3 = [int(round(v)) for v in res.x]
    return {
        "x1": x1,
        "x2": x2,
        "x3": x3,
        "lucro": int(round(-res.fun)),
    }


def plotar_espaco_3d(solucao):
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Malha para os planos de restrição
    x1_vals = np.linspace(0, 4, 30)
    x2_vals = np.linspace(0, 8, 30)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Plano 1: Capitães (x1 + x2 + x3 = 10  =>  x3 = 10 - x1 - x2)
    Z_capitaes = 10.0 - X1 - X2
    Z_capitaes = np.clip(Z_capitaes, 0, 3)

    # Plano 2: Tripulantes (x1 + 2x2 + 3x3 = 18  =>  x3 = (18 - x1 - 2x2)/3)
    Z_tripulantes = (18.0 - X1 - 2.0 * X2) / 3.0
    Z_tripulantes = np.clip(Z_tripulantes, 0, 3)

    # Superfícies semitransparentes dos recursos ativos
    ax.plot_surface(
        X1,
        X2,
        Z_capitaes,
        alpha=0.25,
        color="royalblue",
        label=r"Capitães: $x_1+x_2+x_3 \leq 10$",
    )
    ax.plot_surface(
        X1,
        X2,
        Z_tripulantes,
        alpha=0.30,
        color="darkorange",
        label=r"Tripulantes: $x_1+2x_2+3x_3 \leq 18$",
    )

    # Mapeamento e plotagem de todos os pontos inteiros viáveis
    pontos_x1, pontos_x2, pontos_x3 = [], [], []
    for i in range(5):  # 0 a 4
        for j in range(9):  # 0 a 8
            for k in range(4):  # 0 a 3
                if (i + j + k <= 10) and (i + 2 * j + 3 * k <= 18):
                    pontos_x1.append(i)
                    pontos_x2.append(j)
                    pontos_x3.append(k)

    ax.scatter(
        pontos_x1,
        pontos_x2,
        pontos_x3,
        color="gray",
        alpha=0.35,
        s=20,
        label="Soluções Inteiras Viáveis",
    )

    # Destaque do ponto ótimo analítico
    x_opt = solucao["x1"]
    y_opt = solucao["x2"]
    z_opt = solucao["x3"]
    lucro = solucao["lucro"]

    ax.scatter(
        [x_opt],
        [y_opt],
        [z_opt],
        color="red",
        s=120,
        edgecolors="black",
        linewidth=1.5,
        label=rf"Ótimo $({x_opt}, {y_opt}, {z_opt})$ [$Z^*={lucro}\text{{ marfins}}]$",
    )

    # Vetor de direção de lucro (Gradiente de Z = [50, 70, 100])
    ax.quiver(
        x_opt - 1.0,
        y_opt - 1.4,
        z_opt - 2.0,
        1.0,
        1.4,
        2.0,
        color="crimson",
        length=1.5,
        normalize=True,
        arrow_length_ratio=0.3,
        linewidth=2,
    )
    ax.text(
        x_opt - 0.5,
        y_opt - 1.0,
        z_opt - 1.0,
        "Direção de $\\max Z$",
        color="darkred",
        fontsize=9,
        fontweight="bold",
    )

    # Linhas de projeção do ponto ótimo até os eixos
    ax.plot([x_opt, x_opt], [y_opt, y_opt], [0, z_opt], "r--", linewidth=1.2)
    ax.plot([x_opt, x_opt], [0, y_opt], [0, 0], "r--", linewidth=1.2)
    ax.plot([0, x_opt], [0, 0], [0, 0], "r--", linewidth=1.2)

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 8)
    ax.set_zlim(0, 3)

    ax.set_xlabel(r"Jangadas ($x_1$)", fontsize=11, labelpad=8)
    ax.set_ylabel(r"Supercanoas ($x_2$)", fontsize=11, labelpad=8)
    ax.set_zlabel(r"Arcas ($x_3$)", fontsize=11, labelpad=8)
    ax.set_title(
        "Espaço Tridimensional de Soluções — Capitão Caverna S.A.\n"
        r"$\max Z = 50x_1 + 70x_2 + 100x_3$",
        fontsize=13,
        pad=15,
    )

    ax.view_init(elev=22, azim=130)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sol = resolver_capitao_caverna()
    print("=" * 48)
    print("      RESULTADO ANALÍTICO ÓTIMO (EMBARCAÇÕES)   ")
    print("=" * 48)
    print(f"Jangadas     (x1*) : {sol['x1']} barcos")
    print(f"Supercanoas  (x2*) : {sol['x2']} barcos")
    print(f"Arcas        (x3*) : {sol['x3']} barcos")
    print(f"Lucro Máximo (Z*)  : {sol['lucro']} marfins")
    print("=" * 48)

    plotar_espaco_3d(sol)