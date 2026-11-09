import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


def resolver_pizzaria():
    """Problema da Pizzaria:

    Max Z = 18*x1 + 22*x2  <=>  Min -18*x1 - 22*x2
    sujeito a:
        (1/16)*x1 + (1/9)*x2 <= 24   (Tempo: 3 pizzaiolos * 8h)
        40*x1 + 60*x2 <= 5000        (Queijo: 5 kg = 5000g)
        x1, x2 >= 0
    """
    # Max Z <=> Min (-Z)
    c = [-18.0, -22.0]

    # Matriz A_ub @ x <= b_ub
    A_ub = [
        [1.0 / 16.0, 1.0 / 9.0],  # Mão de obra em horas
        [40.0, 60.0],  # Gramas de queijo
    ]
    b_ub = [24.0, 5000.0]

    bounds = [(0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"Falha na convergência: {res.message}")

    return {
        "x1": float(res.x[0]),
        "x2": float(res.x[1]),
        "receita_max": float(-res.fun),
    }


def plotar_grafico(solucao):
    x1_opt = solucao["x1"]
    x2_opt = solucao["x2"]
    z_opt = solucao["receita_max"]

    # Malha de coordenadas para o plano cartesiano
    x1_vals = np.linspace(0, 420, 1000)
    x2_vals = np.linspace(0, 240, 1000)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Fronteiras das restrições isolando x2:
    # 1. Mão de obra: (1/16)x1 + (1/9)x2 = 24  =>  x2 = 9 * (24 - x1/16) = 216 - 0.5625*x1
    r_tempo = 9.0 * (24.0 - x1_vals / 16.0)

    # 2. Queijo: 40x1 + 60x2 = 5000  =>  x2 = (5000 - 40x1) / 60 = 250/3 - (2/3)x1
    r_queijo = (5000.0 - 40.0 * x1_vals) / 60.0

    fig, ax = plt.subplots(figsize=(11, 7))

    # Plot das linhas de restrição
    ax.plot(
        x1_vals,
        np.maximum(0, r_tempo),
        label=r"Mão de Obra: $\frac{x_1}{16} + \frac{x_2}{9} \leq 24$ (Redundante)",
        color="gray",
        linestyle="--",
        linewidth=1.8,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_queijo),
        label=r"Queijo: $40x_1 + 60x_2 \leq 5.000$ (Ativa)",
        color="royalblue",
        linewidth=2.2,
    )

    # Região factível (delimitada apenas pelo queijo e primeiro quadrante)
    feasible_region = (
        (X1 / 16.0 + X2 / 9.0 <= 24.0)
        & (40.0 * X1 + 60.0 * X2 <= 5000.0)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    ax.imshow(
        feasible_region.astype(int),
        extent=(0, 420, 0, 240),
        origin="lower",
        cmap="Greens",
        alpha=0.25,
    )

    # Retas da Função-Objetivo (Isolucro): 18*x1 + 22*x2 = Z  =>  x2 = -(18/22)*x1 + Z/22
    # 1. Reta intermediária (Z menor)
    z_inter = 1200.0
    ax.plot(
        x1_vals,
        -(18.0 / 22.0) * x1_vals + z_inter / 22.0,
        color="crimson",
        linestyle=":",
        alpha=0.6,
        label=f"F.O. $Z = \\text{{R\\$\\,}}{z_inter:.0f}$",
    )

    # 2. Reta no vértice V3 (0, 83.33)
    z_v3 = 22.0 * (250.0 / 3.0)
    ax.plot(
        x1_vals,
        -(18.0 / 22.0) * x1_vals + z_v3 / 22.0,
        color="crimson",
        linestyle="--",
        alpha=0.6,
        label=f"F.O. $Z = \\text{{R\\$\\,}}{z_v3:.2f}$ (Vértice Calzones)",
    )

    # 3. Reta no ponto ótimo (último ponto de contato antes de sair da região viável)
    ax.plot(
        x1_vals,
        -(18.0 / 22.0) * x1_vals + z_opt / 22.0,
        color="crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima $Z^* = \text{{R\$\,}}{z_opt:.2f}$",
    )

    # Vértices da região viável
    ax.plot(0.0, 0.0, "ko", markersize=5)
    ax.plot(
        0.0,
        250.0 / 3.0,
        "ko",
        markersize=6,
        label=r"Vértice $(0;\, 83{,}33)$",
    )

    # Ponto ótimo destacado
    ax.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=9,
        label=rf"Ótimo $({x1_opt:.0f};\, {x2_opt:.0f})$",
    )

    # Seta indicando o deslocamento para maximização
    ax.annotate(
        "Sentido de Maximização (Crescimento de Z)",
        xy=(130, 20),
        xytext=(180, 80),
        arrowprops=dict(
            facecolor="crimson", shrink=0.08, width=1.5, headwidth=8
        ),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    ax.set_xlim(0, 400)
    ax.set_ylim(0, 230)
    ax.set_xlabel(r"Quantidade de Pizzas ($x_1$)", fontsize=12)
    ax.set_ylabel(r"Quantidade de Calzones ($x_2$)", fontsize=12)
    ax.set_title(
        r"Otimização da Pizzaria: $\max Z = 18x_1 + 22x_2$",
        fontsize=14,
        pad=15,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    resultado = resolver_pizzaria()
    print("=" * 45)
    print("        RESULTADO DA OTIMIZAÇÃO (PIZZARIA)   ")
    print("=" * 45)
    print(f"Pizzas a produzir/vender (x1*)   : {resultado['x1']:.0f} unidades")
    print(f"Calzones a produzir/vender (x2*) : {resultado['x2']:.0f} unidades")
    print(f"Receita Máxima Diária (Z*)       : R$ {resultado['receita_max']:,.2f}")
    print("=" * 45)

    plotar_grafico(resultado)